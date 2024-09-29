import os
import subprocess
import sys

# Get the absolute path of the parent directory of the current script.
parent_dir = os.path.dirname(os.path.abspath(__file__))
# Add the 'pgs2srt' directory to the Python path.
sys.path.append(os.path.join(parent_dir, "libraries", "pgs2srt"))
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import pytesseract
from imagemaker import make_image
from loguru import logger
from pgsreader import PGSReader
from PIL import Image, ImageOps

from mkv_episode_matcher_vob.__main__ import CONFIG_FILE
from mkv_episode_matcher_vob.config import get_config

def convert_mkv_to_sup(mkv_file, output_dir):
    """
    Convert an .mkv file to a .sup file using FFmpeg as primary and mkvextract as a fallback.

    Args:
        mkv_file (str): Path to the .mkv file.
        output_dir (str): Path to the directory where the .sup file will be saved.

    Returns:
        str: Path to the converted .sup file or None if conversion failed.
    """
    # Get the base name of the .mkv file without the extension
    base_name = os.path.splitext(os.path.basename(mkv_file))[0]

    # Construct the output .sup file path
    sup_file = os.path.join(output_dir, f"{base_name}.sup")
    
    if not os.path.exists(sup_file):
        logger.info(f"Processing {mkv_file} to {sup_file}")
        
        # Try FFmpeg command to convert .mkv to .sup
        ffmpeg_cmd = ["ffmpeg", "-i", mkv_file, "-map", "0:s:0", "-c", "copy", sup_file]
        try:
            subprocess.run(ffmpeg_cmd, check=True)
            logger.info(f"Converted {mkv_file} to {sup_file} using FFmpeg")
            return sup_file
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg failed for {mkv_file}: {e}")
            
            # Fallback to mkvextract
            logger.info(f"Trying mkvextract for {mkv_file}")
            # Make sure the output directory exists
            idx_file = os.path.join(output_dir, f"{base_name}.idx")
            sub_file = os.path.join(output_dir, f"{base_name}.sub")
            english_track_id = get_english_subtitle_track(mkv_file)
            mkvextract_cmd = ["mkvextract", "tracks", mkv_file, f"{english_track_id}:{sub_file}"]
            try:
                subprocess.run(mkvextract_cmd, check=True)
                logger.info(f"Extracted subtitles for {mkv_file} using mkvextract")
                if os.path.exists(sub_file) and os.path.exists(idx_file):
                    # Convert .sub/.idx to .sup using BDSup2Sub
                    config = get_config(CONFIG_FILE)
                    bdsup2sub_jar_path = config.get("BDSup2Sub_path") 
                    bdsup2sub_cmd = [
                        'java', '-jar', bdsup2sub_jar_path,
                        sub_file,  # Input .sub file
                        '-o', sup_file  # Output file
                    ]
                    try:
                        subprocess.run(bdsup2sub_cmd, check=True, capture_output=True, text=True)
                        logger.info(f"Converted {sub_file} and {idx_file} to {sup_file}")
                    
                        # Clean up temporary files
                        os.remove(sub_file)
                        os.remove(idx_file)
                    
                        return sup_file
                    except subprocess.CalledProcessError as e:
                        logger.error(f"SubtitleEdit conversion failed for {sub_file}: {e}")
                        logger.error(f"SubtitleEdit output: {e.output}")
                else:
                    logger.error(f"Missing .sub or .idx file for {mkv_file}")
            except subprocess.CalledProcessError as e:
                logger.error(f"mkvextract failed for {mkv_file}: {e}")
                return None
    else:
        logger.info(f"File {sup_file} already exists, skipping")
        return sup_file

def get_english_subtitle_track(mkv_file):
    """
    Get the track ID of the English subtitle track from an MKV file.

    This function runs the `mkvinfo` command to parse the available tracks
    in the specified MKV file. It searches for subtitle tracks labeled
    as "English" and returns the corresponding track ID.

    Args:
        mkv_file (str): Path to the MKV file.

    Returns:
        str: The track ID of the English subtitle track.
        
    """
    try:
        # Run mkvinfo to get track information
        output = subprocess.check_output(["mkvinfo", mkv_file], text=True) 
       
        english_track_id = None

        # Parse the output line by line
        lines = output.splitlines()
        for i, line in enumerate(lines):
            # Check if the line contains a subtitle track
            if "Track type: subtitles" in line:
                # Look ahead in lines to get the language information
                for j in range(i, i+10):  # assuming language line appears within next 10 lines
                    if "Language: eng" in lines[j]:
                        # Retrieve the track ID from earlier in lines
                        for k in range(i, 0, -1):  # going backwards to find track ID
                            if "Track number:" in lines[k]:
                                # Extract the mkvextract track ID from the line
                                parts = lines[k].split(" ")
                                english_track_id = parts[-1].strip('()')
                                
                                # Print the entire track info to console
                                track_info = "\n".join(lines[i:k+7])  # Collecting track-related lines
                                print("Found english subtitle:"+track_info+"; track_id: "+ english_track_id)
                                                                
                                return english_track_id
        return None  # If no English subtitle track is found
    
    except subprocess.CalledProcessError as e:
        print(f"Error running mkvinfo: {e}")
        raise

@logger.catch
def perform_ocr(sup_file_path):
    """
    Perform OCR on a .sup file and save the extracted text to a .srt file.

    Args:
        sup_file_path (str): Path to the .sup file.
    """

    # Get the base name of the .sup file without the extension
    base_name = os.path.splitext(os.path.basename(sup_file_path))[0]
    output_dir = os.path.dirname(sup_file_path)
    logger.info(f"Performing OCR on {sup_file_path}")
    # Construct the output .srt file path
    srt_file = os.path.join(output_dir, f"{base_name}.srt")

    # Load a PGS/SUP file.
    pgs = PGSReader(sup_file_path)

    # Set index
    i = 0

    # Complete subtitle track index
    si = 0

    tesseract_lang = "eng"
    tesseract_config = f"-c tessedit_char_blacklist=[] --psm 6 --oem {1}"

    config = get_config(CONFIG_FILE)
    tesseract_path = config.get("tesseract_path")
    logger.debug(f"Setting Teesseract Path to {tesseract_path}")
    pytesseract.pytesseract.tesseract_cmd = str(tesseract_path)

    # SubRip output
    output = ""

    if not os.path.exists(srt_file):
        # Iterate the pgs generator
        for ds in pgs.iter_displaysets():
            # If set has image, parse the image
            if ds.has_image:
                # Get Palette Display Segment
                pds = ds.pds[0]
                # Get Object Display Segment
                ods = ds.ods[0]

                if pds and ods:
                    # Create and show the bitmap image and convert it to RGBA
                    src = make_image(ods, pds).convert("RGBA")

                    # Create grayscale image with black background
                    img = Image.new("L", src.size, "BLACK")
                    # Paste the subtitle bitmap
                    img.paste(src, (0, 0), src)
                    # Invert images so the text is readable by Tesseract
                    img = ImageOps.invert(img)

                    # Parse the image with tesesract
                    text = pytesseract.image_to_string(
                        img, lang=tesseract_lang, config=tesseract_config
                    ).strip()

                    # Replace "|" with "I"
                    # Works better than blacklisting "|" in Tesseract,
                    # which results in I becoming "!" "i" and "1"
                    text = re.sub(r"[|/\\]", "I", text)
                    text = re.sub(r"[_]", "L", text)
                    start = datetime.fromtimestamp(ods.presentation_timestamp / 1000)
                    start = start + timedelta(hours=-1)

            else:
                # Get Presentation Composition Segment
                pcs = ds.pcs[0]

                if pcs:
                    end = datetime.fromtimestamp(pcs.presentation_timestamp / 1000)
                    end = end + timedelta(hours=-1)

                    if (
                        isinstance(start, datetime)
                        and isinstance(end, datetime)
                        and len(text)
                    ):
                        si = si + 1
                        sub_output = str(si) + "\n"
                        sub_output += (
                            start.strftime("%H:%M:%S,%f")[0:12]
                            + " --> "
                            + end.strftime("%H:%M:%S,%f")[0:12]
                            + "\n"
                        )
                        sub_output += text + "\n\n"

                        output += sub_output
                        start = end = text = None
            i = i + 1
        with open(srt_file, "w") as f:
            f.write(output)
        logger.info(f"Saved to: {srt_file}")

def convert_mkv_to_srt(season_path, mkv_files):
    """
    Converts MKV files to SRT format.

    Args:
        season_path (str): The path to the season directory.
        mkv_files (list): List of MKV files to convert.

    Returns:
        None
    """
    logger.info(f"Converting {len(mkv_files)} files to SRT")
    output_dir = os.path.join(season_path, "ocr")
    os.makedirs(output_dir, exist_ok=True)
    sup_files = []
    for mkv_file in mkv_files:
        sup_file = convert_mkv_to_sup(mkv_file, output_dir)
        sup_files.append(sup_file)
    with ThreadPoolExecutor() as executor:
        for sup_file in sup_files:
            executor.submit(perform_ocr, sup_file)
