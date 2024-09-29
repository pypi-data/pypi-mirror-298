=======================
MKV Episode Matcher VOB
=======================

|docs|  |pypi|

The MKV Episode Matcher VOB is a fork of `MKV Episode Matcher <https://github.com/Jsakkos/mkv-episode-matcher>`_ for identifying TV series episodes from MKV files and renaming the files accordingly with additional support for VOB files, which are typically found in DVDs.

Quick start
===========

To use the MKV Episode Matcher, follow these steps:

1. Install ``pip install mkv-episode-matcher-vob``
2. Obtain an API key from TMDb (https://developers.themoviedb.org/authentication/getting-a-apikey).
3. (Optional) - Obtain an API key from Opensubtitles.com by creating an API consumer (https://www.opensubtitles.com/en/consumers)
4. Alternatively, add the .srt files to the cache directory. On Windows: ``C:\Users\YOUR_USER_NAME\.mkv-episode-matcher\cache\data\SHOW_NAME``. The files need to be named with the season and episode, e.g. ``Show Name - S01E01.srt``.
5. Provide a filepath to your show directory. This is the main directory that contains all of the episodes for a specific show.

The directory and subfolders must be arranged in the following structure:

- Show name
  - Season 1
  - Season 2
  - ...
  - Season n
  
6. Call ``mkv-match`` with the TMDB_API_KEY and SHOW_DIR as arguments or in environment variables from your command line:

.. code-block:: bash

   python mkv-match --tmdb-api-key your-api-key --show-dir /path/to/show

Once TMDB_API_KEY is set, there's no need to enter it again, as it gets stored in the config.ini file.

To get subtitles from opensubtitles.com, ensure that the appropriate credentials have been set, either via the CLI or in config.ini (On Windows: ``C:\Users\YOUR_USER_NAME\.mkv-episode-matcher\config.ini``).
Then add the ``--get-subs True`` flag to the CLI call

.. code-block:: bash

   python mkv-match --show-dir /path/to/show --get-subs True

7. For VOBSub: The VOBSub can't be handled by FFmpeg, so you also need to download ``MKVToolNix`` (for mkvextract and mkvinfo) and ``BDSup2Sub``. 
The latter needs a path specification to the ``BDSup2Sub.exe`` in the config.ini file.

Troubleshooting 
===============

1. Make sure that all the necessary tools are installed and properly linked.

2. Check your config.ini file. Here is an example structure (MacOS): 

::

   [Config]
   tmdb_api_key = YOUR_TMDB_KEY
   open_subtitles_api_key = YOUR_OPEN-SUBTITLES_KEY
   open_subtitles_user_agent = YOUR_API-CONSUMER_NAME
   open_subtitles_username = YOUR_OPEN-SUBTITLES_USERNAME
   open_subtitles_password = YOUR_OPEN-SUBTITLES_USERPASSWORD
   bdsup2sub_path = /Applications/BDSup2Sub512.jar

3. It may be necessary to also add the path for tesseract to your config.ini. Here is an example for a hombrew installtion:

.. code-block:: bash

  tesseract_path = /opt/homebrew/Cellar/tesseract/5.4.1/bin/tesseract

(Note how the path leads to the tesseract executable)

How it works
============

MKV Episode Matcher extracts the subtitle text from each MKV file, then cross-references the text against .srt subtitle files that are either user-provided or downloaded from Opensubtitles.com.

License
=======

MIT License

Copyright (c) 2024 Jonathan Sakkos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Acknowledgments
===============

This product uses the TMDB API but is not endorsed or certified by TMDB.

.. image:: https://www.themoviedb.org/assets/2/v4/logos/v2/blue_long_2-9665a76b1ae401a510ec1e0ca40ddcb3b0cfe45f1d51b77a308fea0845885648.svg
   :alt: The Movie Database
   :target: https://www.themoviedb.org/

.. |docs| image:: https://readthedocs.org/projects/mkv-episode-matcher/badge/?version=latest
   :target: https://mkv-episode-matcher.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. |pypi| image:: https://badge.fury.io/py/mkv-episode-matcher.svg
   :target: https://badge.fury.io/py/mkv-episode-matcher
