## gif2ascii

#### Example using command line

```bash
python -m gif2ascii -f anime.gif -w 80
python -m gif2ascii -f anime.gif --fit-terminal
python -m gif2ascii -f hehe.jpg -c ABCDEF -d 0.1
```

#### Example using Code

```python
from gif2ascii import GifAscii

file_name = 'test.gif'
width = 80
GifAscii(file_name, width).output()
```

#### Available Options to constructor
```
file_name - Name of the file to convert
-- optional params --
width - width in chars for output
frame_delay - Delay between frames in GIF while rendering to terminal
fit_terminal - Ignores width, takes the entire terminal size
chars - specify chars for ASCII text (fat characters gives better results)
loop_gif - you know what it is :p (ctrl + c to end)
```

