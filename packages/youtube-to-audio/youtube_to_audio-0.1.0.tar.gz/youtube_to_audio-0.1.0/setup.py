from setuptools import setup, find_packages

setup(
    name="youtube-to-audio",
    version="0.1.0",
    description="A Python package to extract audio from a YouTube video in multiple formats.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jack Tol",
    author_email="contact@jacktol.net",
    url="https://github.com/jack-tol/youtube-to-audio",
    packages=find_packages(),
    install_requires=[
        "pytubefix",
        "moviepy",
        "argparse",
        "pytest"
    ],
    entry_points={
        'console_scripts': [
            'youtube-to-audio=youtube_to_audio.cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
