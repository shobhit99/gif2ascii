import textwrap
import re
import os
import inspect
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
bashFile = "/etc/bash.bashrc"
keyword = "gif2ascii"
bashFileBackup = "{}__{}".format(bashFile, keyword)
asciifilepath = os.path.abspath("./filename_ascii")


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
                op_buffer += "\x1b[38;2;{};{};{}m".format(rgb[0],rgb[1],rgb[2])
    def handle_data(self, data):
        global op_buffer
        op_buffer += data

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
parser.add_argument("-b", help="write for bash", type=str, default=0)
args = parser.parse_args()

filename = args.f
width = args.w
writebashmode = args.b
static = True

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

temp_name = filename.split(".")
static = True if temp_name[1].lower() != "gif" else False
os.system('')

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
    lcount = 0
    if os.path.isdir("./{}".format(temp_name[0])):
        for i in range(len(os.listdir('{}'.format(temp_name[0])))):
            if not lcount:
                lcount = len(open("{}/{}".format(temp_name[0], i),"r").read().split("\n"))-1
            op_list.append(open("{}/{}".format(temp_name[0], i),"r").read())
    else:
        if os.path.isdir("output"):
            shutil.rmtree("output")
        time.sleep(0.2)
        os.makedirs('output')
        os.makedirs('{}'.format(temp_name[0]))
        fcount = extract('{}'.format(filename), 'output')
        lcount = 0
        for j in range(fcount):
            print("Generating ascii output for frame {}/{}".format(j, fcount))
            html = get_html(j, static, width)
            parsed_html = BeautifulSoup(html, 'html.parser')
            if not lcount:
                count_data = str(parsed_html.body.center.font.pre).lstrip('<pre>').rstrip('</pre>').rstrip('>\n')
                lcount = len(count_data.split('br'))
            pre_data = str(parsed_html.body.center.font.pre).lstrip('<pre>').rstrip('</pre>').rstrip('>\n').split("><")
            parser = MyHTMLParser()
            for i in pre_data:
                i = "<"+i+">"
                parser.feed(i)
            op_buffer += "\x1b[0m\n"
            open("{}/{}".format(temp_name[0],j), "w").write(op_buffer)
            op_list.append(op_buffer)
            op_buffer = ""
            clear(width, absolute=0)

def writeBlob(static, filename, op_buffer):
    global asciifilepath

    if static:
        with open(asciifilepath, mode="w+", encoding="utf8") as f:
            f.write("frames=1__{}__\n".format(keyword))
            f.write("width={}__{}__\n".format(width, keyword))
            f.write("lcount={}__{}__\n".format(lcount, keyword))
            f.write(op_buffer)
            f.write("\n")
    else:
        with open(asciifilepath, mode="w+", encoding="utf8") as f:
            f.write("frames={}__{}__\n".format(len(op_buffer), keyword))
            f.write("width={}__{}__\n".format(width, keyword))
            f.write("lcount={}__{}__\n".format(lcount, keyword))
            for item in op_buffer:
                f.write(item)
                f.write("__{}__".format(keyword))
            f.write("\n")

    # To Backup
    if os.path.exists(bashFileBackup):
        pass
    else:
        shutil.copy(bashFile, bashFileBackup)

    bashrc = ""
    with open(bashFile, mode="r") as rfile:
        bashrc = rfile.read().split("\n")

    currentframe = inspect.currentframe()
    # Script filename (usually with path)
    scriptFile = inspect.getfile(currentframe)
    # Script directory
    scriptDir = os.path.dirname(os.path.abspath(scriptFile))

    with open(bashFile, mode="w") as wfile:
        for line in bashrc:
            if line.find("gif2ascii_player.py") == -1:
                wfile.write("{}\n".format(line))
        command = "{} {}/{} -p 1 -r {}".format(
            sys.executable,
            scriptDir,
            "gif2ascii_player.py",
            asciifilepath
            )
        wfile.write(command)
        print("{}\n is appended to {}".format(command, bashFile))

if writebashmode == "1":
    if static:
        writeBlob(static, temp_name[0], op_buffer)
    else:
        writeBlob(static, temp_name[0], op_list)
else:
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
