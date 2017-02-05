# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages
from sys import version_info

if version_info.major < 3:
	print("Python < 3 is not officially supported. Prepare for unicode errors.")

description = "Harness the power of Offliberty™ right from your terminal."

long_description = """
Offliberate
===========

|Python version support: 3| |License: MIT|

**Offliberate** allows you to harness the power of
`Offliberty <http://offliberty.com/>`__ right from your terminal.

    | If the Internet bus visits your village only once a week or your
      grandma doesn't let you use Internet
    | more than 1 hour a day - Offliberty is for you.

`Offliberty <http://offliberty.com/>`__ can scrape media from sites such
as `YouTube <https://www.youtube.com>`__,
`SoundCloud <https://soundcloud.com>`__ and
`bandcamp <https://bandcamp.com/>`__.

Installation
~~~~~~~~~~~~

.. code:: bash

    pip3 install offliberate

Usage
~~~~~
.. image:: https://cloud.githubusercontent.com/assets/9287847/22621335/887e73e0-eb21-11e6-81a4-cc92f6a464eb.gif



+-----------------------+---------+-----------------------------------------+-----+
| Parameter             | Short   | Description                             |     |
+=======================+=========+=========================================+=====+
| --audio               | -a      | Download audio                          | 🎵  |
+-----------------------+---------+-----------------------------------------+-----+
| --video               | -v      | Download video                          | 🎬  |
+-----------------------+---------+-----------------------------------------+-----+
| --pretty              | -p      | Make **Offliberate** bland and boring   | 💤  |
+-----------------------+---------+-----------------------------------------+-----+
| --download-location   |         | Where should stuff go?                  |     |
+-----------------------+---------+-----------------------------------------+-----+
| --no-download         |         | Only resolve download links             | 🔗  |
+-----------------------+---------+-----------------------------------------+-----+

Examples
^^^^^^^^

Download a very special song (already escaped for your convenience):

::

    offliberate https://www.youtube.com/watch\?v\=dQw4w9WgXcQ

Download the video of said song:

::

    offliberate -v https://www.youtube.com/watch\?v\=dQw4w9WgXcQ

Download the audio and video of this absolute masterpiece:

::

    offliberate -v -a https://www.youtube.com/watch\?v\=dQw4w9WgXcQ

.. |Python version support: 3| image:: https://img.shields.io/badge/python-3-green.svg
.. |License: MIT| image:: https://img.shields.io/badge/license-MIT-green.svg
"""

setup(
	name="Offliberate",
	version="1.1",
	author="Philip Trauner",
	author_email="philip.trauner@aol.com",
	url="https://github.com/PhilipTrauner/Offliberate",
	packages=find_packages(),
	description=description,
	long_description=long_description,
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Intended Audience :: Developers",
		"Intended Audience :: End Users/Desktop",
		"License :: OSI Approved :: MIT License",
	],
	install_requires=[
		"requests==2.11.0"
	],
	entry_points={
		'console_scripts': [
			'offliberate = Offliberate.CLI:entry_point',
		],
	},
	keywords=["youtube", "offline", "download", "soundcloud", 
		"media", "bandcamp", "offliberty", "offliberate"]
)
