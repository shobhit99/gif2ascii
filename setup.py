from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.3'
DESCRIPTION = 'Gif to ASCII'
LONG_DESCRIPTION = 'Converts Gifs and Images to Colorful ASCII'

# Setting up
setup(
    name="gif2ascii",
    version=VERSION,
    author="Shobhit Bhosure",
    author_email="<shobhitbhosure7@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['Pillow', 'argparse'],
    keywords=['python', 'ascii gif', 'terminal gif', 'ascii art', 'terminal art'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
