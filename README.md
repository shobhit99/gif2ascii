## gif2ascii


https://user-images.githubusercontent.com/38807205/230733470-5491dd82-5e36-4f73-b553-a38a167837ec.mov


#### Example using command line

```bash
python -m gif2ascii -f anime.gif -w 80
python -m gif2ascii -f anime.gif --fit-terminal
python -m gif2ascii -f hehe.jpg -c ABCDEF -d 0.1
```

#### Example using Code

```python
from gif2ascii import GifAscii

file_name = 'jujutsu.gif'
width = 80
GifAscii(file_name, width).output()
```

#### Available Options to constructor
```
usage: python -m gif2ascii [-h] -f F [-w W] [-d D] [-c C] [--fit-terminal] [--no-loop] [--screenfetch]

Gif to Ascii

options:
  -h, --help      show this help message and exit
  -f F            Input file, static image or gif file
  -w W            Width in chars
  -d D            Frame delay between frames for gif
  -c C            Characters to be used for ASCII output
  --fit-terminal  Fit entire terminal
  --no-loop       Loop gif animation
  --screenfetch   Create template for screenfetch

	Examples:

    python -m gif2ascii -f anime.gif -w 80
    python -m gif2ascii -f anime.gif --fit-terminal
    python -m gif2ascii -f john.jpg -c ABCDEF -d 0.1

    Use with screenfetch

    echo 'startline=0;fulloutput=($(python -m gif2ascii -f john.jpg -w 40 --screenfetch))' > /tmp/script.sh && screenfetch -E -a /tmp/script.sh

    github.com/shobhit99
```

