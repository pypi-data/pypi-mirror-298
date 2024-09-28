from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.1.3'
DESCRIPTION = 'RedditReader - Let your stories come to life'
LONG_DESCRIPTION = 'A package that allows you to package a reddit url https://reddit.com/* with a youtube video, for free, add subtitles and publish it!'

# Setting up
setup(
    name="Redreader",
    version=VERSION,
    author="Aghastmuffin",
    author_email="helpredditreader@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['PyQt6', 'moviepy', 'vosk', 'pyttsx3', 'yt_dlp'],
    keywords=['python', 'video', 'stream', 'RedditReader', 'Read Reddit', 'Stories', 'automated readreddit'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)