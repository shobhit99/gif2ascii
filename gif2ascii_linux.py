import textwrap
import re
import os
import sys
import time
import getpass
import subprocess
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
static = False
attrs_machine = []

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
            global static
            global attrs_machine
            if attrs_machine != []:
                op_buffer += "    \x1b[0m" + attrs_machine.pop() + "\n"
            else:
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

	'''
parser = argparse.ArgumentParser(description="Virtual Box Script", epilog=usage, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-f", help="input file", type=str)
parser.add_argument("-w", help="width for output", type=str, default=50)
args = parser.parse_args()

filename = args.f
width = args.w

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

temp_name = filename.split(".")
static = True if temp_name[1].lower() != "gif" else False
os.system('')
output = subprocess.check_output('screenfetch', shell=True)
output = output.decode('utf-8')
osystem = re.findall(r'OS\:.{5}(.*)', output)[0][:-4]
kernel = re.findall(r'Kernel\:.{5}(.*)', output)[0][:-4]
uptime = re.findall(r'Uptime\:.{5}(.*)', output)[0][:-4]
packages = re.findall(r'Packages\:.{5}(.*)', output)[0][:-4]
shell = re.findall(r'Shell\:.{5}(.*)', output)[0][:-4]
resolution = re.findall(r'Resolution\:.{5}(.*)', output)[0][:-4]
de = re.findall(r'DE\:.{5}(.*)', output)[0][:-4]
font = re.findall(r'Font\:.{5}(.*)', output)[0][:-4]
cpu = re.findall(r'CPU\:.{5}(.*)', output)[0][:-4]
gpu = re.findall(r'GPU\:.{5}(.*)', output)[0][:-4]
ram = re.findall(r'RAM\:.{5}(.*)', output)[0][:-4]
attrs_machine.extend(["\x1b[38;2;255;255;255mUser: \x1b[0m"+getpass.getuser(),"\x1b[38;2;255;255;255mOS: \x1b[0m"+osystem, "\x1b[38;2;255;255;255mKernel: \x1b[0m"+kernel, "\x1b[38;2;255;255;255mUptime: \x1b[0m"+uptime,
    "\x1b[38;2;255;255;255mPackages: \x1b[0m"+packages, "\x1b[38;2;255;255;255mShell: \x1b[0m"+shell, 
"\x1b[38;2;255;255;255mResolution: \x1b[0m"+resolution, "\x1b[38;2;255;255;255mDE: \x1b[0m"+de, "\x1b[38;2;255;255;255mFONT: \x1b[0m"+font, 
"\x1b[38;2;255;255;255mCPU: \x1b[0m"+cpu, "\x1b[38;2;255;255;255mGPU: \x1b[0m"+gpu, "\x1b[38;2;255;255;255mRAM: \x1b[0m"+ram][::-1])

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
            print("Generating ascii output for frame {}".format(j))
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

if static:
    sys.stdout.write(op_buffer)
else:
    try:
        while True:
            for i in op_list:
                sys.stdout.write(i)
                time.sleep(0.1)
                clear(width, absolute=lcount-1)
    except KeyboardInterrupt:
        print("\x1b[0m\n")