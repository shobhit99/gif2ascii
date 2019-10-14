import argparse
import multiprocessing
import os
import requests
import shutil
import sys
import textwrap
import time

from bs4 import BeautifulSoup
from clear import clear
from html.parser import HTMLParser
from PIL import Image
from textimage import get_html
import urllib3
from webcolors import name_to_rgb

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

op_list = []
op_buffer = ""

session = None


def set_global_session():
    global session
    if not session:
        session = requests.Session()


def hex_to_rgb(value):
    value = value[1:]
    len_value = len(value)
    if len_value == 3:
        value = ''.join(i * 2 for i in value)
    return tuple(int(i, 16) for i in textwrap.wrap(value, 2))


def extract(inGif, outFolder):
    frame = Image.open(inGif)
    nframes = 0
    while frame:
        frame.save('{}/{}.gif'.format(outFolder, nframes ) , 'GIF')
        nframes += 1
        try:
            frame.seek( nframes )
        except EOFError:
            break;
    return nframes


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if "br" in tag:
            global op_buffer
            op_buffer += "\n"
        else:
            for attr in attrs:
                if "#" != attr[1][0]:
                    rgb = name_to_rgb(attr[1])
                else:
                    rgb = hex_to_rgb(attr[1])
                op_buffer += "\x1b[38;2;{};{};{}m".format(rgb[0], rgb[1], rgb[2])

    def handle_data(self, data):
        global op_buffer
        op_buffer += data


usage = '''
    Example:
    
    For Gifs
    python gif2ascii.py -f image.gif -w 40

    For Static images
    python gif2ascii.py -f image.jpg -w 100 --static

    '''
parser = argparse.ArgumentParser(description="Gif to Ascii", epilog=usage, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-f", help="input file", type=str)
parser.add_argument("-w", help="width for output", type=str, default=50)
args = parser.parse_args()

filename = args.f
width = args.w
static = True

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

temp_name = filename.split(".")
static = True if temp_name[1].lower() != "gif" else False
os.system('')


br_count = 0
op_list = []
op_buffer = ""


def get_frame(frame_count):
    global br_count, op_list, op_buffer

    print("Generating ascii output for frame {}".format(frame_count))
    frame_html = get_html(frame_count, static, width)
    parsed_frame_html = BeautifulSoup(frame_html, 'html.parser')
    if not br_count:
        html_count_data = str(parsed_frame_html.body.center.font.pre).lstrip('<pre>').rstrip('</pre>').rstrip('>\n')
        br_count = len(html_count_data.split('br'))
    initial_data = str(parsed_frame_html.body.center.font.pre).lstrip('<pre>').rstrip('</pre>').rstrip('>\n').split("><")
    html_parser = MyHTMLParser()
    for data in initial_data:
        data = "<" + data + ">"
        html_parser.feed(data)
    op_buffer += "\x1b[0m\n"
    open("{}/{}".format(temp_name[0], frame_count), "w").write(op_buffer)
    op_list.append(op_buffer)
    op_buffer = ""
    clear(width, absolute=0)


def get_lcount(count=0):
    for idx in range(len(os.listdir('{}'.format(temp_name[0])))):
        if not count:
            count = len(open("{}/{}".format(temp_name[0], idx), "r").read().split("\n")) - 1
        print("{}/{}".format(temp_name[0], idx))
        op_list.append(open("{}/{}".format(temp_name[0], idx), "r").read())
    return count


if static:
    html = get_html(filename, static, width)
    parsed_html = BeautifulSoup(html, 'html.parser')
    count_data = str(parsed_html.body.center.font.pre).lstrip('<pre>').rstrip('</pre>').rstrip('>\n')
    lcount = len(count_data.split('br'))
    pre_data = str(parsed_html.body.center.font.pre).lstrip('<pre>').rstrip('</pre>').rstrip('>\n').split("><")
    parser = MyHTMLParser()
    for i in pre_data:
        i = "<"+i+">"
        parser.feed(i)
    op_buffer += "\x1b[0m\n"
else:
    if os.path.isdir("./{}".format(temp_name[0])):
        lcount = get_lcount()
    else:
        if os.path.isdir("output"):
            shutil.rmtree("output")
        time.sleep(0.2)
        os.makedirs('output')
        os.makedirs('{}'.format(temp_name[0]))
        frame_count = extract('{}'.format(filename), 'output')
        lcount = 0

        with multiprocessing.Pool(initializer=set_global_session) as pool:
            result = pool.map(get_frame, [i for i in range(frame_count)])

        if not list(filter(None, result)):
            lcount = get_lcount()


if static:
    sys.stdout.write(op_buffer)
else:
    try:
        while True:
            for i in op_list:
                sys.stdout.write(i)
                time.sleep(0.08)
                clear(width, absolute=lcount-1)
    except KeyboardInterrupt:
        print("\x1b[0m\n")
