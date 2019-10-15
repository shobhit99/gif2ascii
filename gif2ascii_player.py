import textwrap
import re
import os
import sys
import time
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from webcolors import name_to_rgb
from textimage import get_html
import urllib3
import argparse
from PIL import Image
from clear import clear
import shutil
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

op_list = []
op_buffer = ""

usage = '''
	Example:

    For Gifs
    python gif2ascii.py -f image.gif -w 40

    For Static images
    python gif2ascii.py -f image.jpg -w 100 --static

    To show when Bash terminal start (Linux)
    sudo python gif2ascii.py -f image.jpg -w 60 -b 1
    sudo python gif2ascii.py -f image.gif -w 60 -b 1

	'''
parser = argparse.ArgumentParser(description="Gif to Ascii", epilog=usage, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-f", help="input file", type=str)
parser.add_argument("-w", help="width for output", type=str, default=50)
parser.add_argument("-p", help="for play when bash starts", type=str, default=0)
parser.add_argument("-r", help="ascii file path", type=str, default="~/filename_ascii")
args = parser.parse_args()

filename = args.f
width = args.w
readbashmode = args.p
asciifilepath = args.r
static = True
lcount = 0
width = 50

def readBlob():
    global lcount, width
    with open("{}".format(asciifilepath), mode='r', encoding='utf8') as f:
        content = f.read()
        farr = content.split("__gif2ascii__")
        if farr[0] == "frames=1":
            return True, farr[3], None
        else:
            width = farr[1].replace("width=", "")
            width = int(width)
            lcount = farr[2].replace("lcount=", "")
            lcount = int(lcount)
            return False, None, farr[3:]

if readbashmode == '1':
    static, op_buffer, op_list = readBlob()

if static:
    sys.stdout.write(op_buffer)
else:
    try:
        while True:
            for i in op_list:
                sys.stdout.write(i)
                time.sleep(0.08)
                clear(width, absolute=lcount-1)
            break
    except KeyboardInterrupt:
        print("\x1b[0m\n")
