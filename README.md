## gif2ascii
> Requires python3.7 
### Installation
```bash
python3.7 -m pip install -r requirements.txt
# for linux (optional)
sudo apt-get install screenfetch
```
### Usage
```bash
# Generates single ascii file for images (jpeg/png)
python3.7 gif2ascii.py -f image.jpg -w 60 
# Generates ascii for every frame ( takes time depending upon frame count)
python3.7 gif2ascii.py -f image.gif -w 60
# Print help
python3.7 gif2ascii.py -h
```
