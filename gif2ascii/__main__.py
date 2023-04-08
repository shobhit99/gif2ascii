import argparse

from gif2ascii.GifAscii import GifAscii

usage = '''

	Examples:
	
    python -m gif2ascii -f anime.gif -w 80
    python -m gif2ascii -f anime.gif --fit-terminal
    python -m gif2ascii -f john.jpg -c ABCDEF -d 0.1

    Use with screenfetch

    echo 'startline=0;fulloutput=($(python -m gif2ascii -f john.jpg -w 40 --screenfetch))' > /tmp/script.sh && screenfetch -E -a /tmp/script.sh

    github.com/shobhit99
'''

parser = argparse.ArgumentParser(description="Gif to Ascii", epilog=usage, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-f", help="Input file, static image or gif file", type=str, required=True)
parser.add_argument("-w", help="Width in chars", type=str, default=80)
parser.add_argument("-d", help="Frame delay between frames for gif", type=str, default=0.05)
parser.add_argument("-c", help="Characters to be used for ASCII output", type=str, default="108BRES")
parser.add_argument("--fit-terminal", help="Fit entire terminal", action='store_true', default=False)
parser.add_argument("--no-loop", help="Loop gif animation ", action='store_true', default=False)
parser.add_argument("--screenfetch", help="Create template for screenfetch", action='store_true', default=False)

args = parser.parse_args()

GifAscii(
    file_name=args.f,
    width=int(args.w),
    frame_delay=float(args.d),
    chars=args.c,
    fit_terminal=args.fit_terminal,
    loop_gif=not args.no_loop,
    screenfetch=args.screenfetch
).output()
