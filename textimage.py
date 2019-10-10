import requests
import warnings
import sys

url = "https://text-image.com/convert/pic2html.cgi"

def get_html(filename, static, width=120):
    if static:
        pass
    else:
        filename = "output/{}.gif".format(filename)
    with open("{}".format(filename), 'rb') as f:
        headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language' : 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        }
        files = {'image':f,
            "characters" : (None, '01'),
            "textType" : (None, 'random'),
            "fontsize" : (None, '-3'),
            "width" : (None, '{}'.format(width)),
            "grayscale" : (None, '0'),
            "bgcolor" : (None, 'BLACK'),
            "contrast" : (None, '0'),
            "browser" : (None, 'firefox')
            }
        r = requests.post(url, files=files, headers=headers, verify=False)
        return str(r.text)