import random
import sys
import time

from PIL import Image
from shutil import get_terminal_size

from gif2ascii.clear import clear


class GifAscii:
    
    def __init__(self, file_name, width=80, chars=list('108BRES'), frame_delay=0.05, loop_gif=True, fit_terminal=False, screenfetch=False):
        self.file_name = file_name
        self.op_width = width
        self.chars = chars
        self.tsize = get_terminal_size()
        self.op_height = None
        self.screenfetch = screenfetch
        if fit_terminal:
            self.op_width = self.tsize.columns
            self.op_height = self.tsize.lines
        self.gif_frame_delay = frame_delay
        self.loop_gif = loop_gif

    def is_gif(self):
        """
            Returns if provided file is gif or not based on extension
        """
        temp_file_name = self.file_name.split('.')
        if len(temp_file_name) > 1:
            if temp_file_name[-1].lower() == 'gif':
                return True
        return False

    def get_ansi(self):
        """
            Returns ANSI output, which can be directly dumped on terminal using sys.stdout.write
        """
        if self.is_gif():
            return self.extract_frames()
        else:
            op_buffer = ''
            with Image.open(self.file_name) as image:
                op_height = self.op_height or int((image.height // (image.width / self.op_width)) // 2.3)
                image = image.resize((self.op_width, op_height))
                width, height = image.width, image.height
                for i in range(height):
                    for j in range(width):
                        pixel = image.getpixel((j, i))
                        r, g, b = self.get_rgb(pixel, image)
                        op_buffer += '\x1b[38;2;{};{};{}m'.format(r, g, b)
                        op_buffer += str(self.chars[random.randint(0, len(self.chars)-1)])
                    op_buffer += '%s\n' if self.screenfetch else '\n'
            return op_buffer
    
    def _get_gif_frame_ansi(self, image):
        """
            Takes single image object of gif and returns ANSI
        """
        op_height = self.op_height or int((image.height // (image.width / self.op_width)) // 2.3)
        image = image.resize((self.op_width, op_height))
        width, height = image.width, image.height
        op_buffer = ''
        for i in range(height):
            for j in range(width):
                pixel = image.getpixel((j, i))
                r, g, b = self.get_rgb(pixel, image)
                op_buffer += '\x1b[38;2;{};{};{}m'.format(r, g, b)
                op_buffer += str(self.chars[random.randint(0, len(self.chars)-1)])
            op_buffer += '\n'
        return op_buffer
    
    def output(self):
        """
            writes the ANSI output to screen
        """
        if not self.is_gif():
            sys.stdout.write(self.get_ansi())
        else:
            self.output_gif()
    
    def play_gif(self, frames):
        """
            Plays one iteration of gif
        """
        for frame in frames:
            sys.stdout.write(frame)
            time.sleep(self.gif_frame_delay)
            clear(self.op_width, self.tsize.lines)
    
    def output_gif(self):
        """
            start gif animation with or without loop
        """
        frames = self.extract_frames()
        if self.loop_gif:
            try:
                while True:
                    self.play_gif(frames)
            except KeyboardInterrupt:
                pass
        else:
            self.play_gif(frames)
    
    def get_rgb(self, pixel, image):
        if isinstance(pixel, int):
            palette = image.getpalette()
            color_idx = pixel * 3
            r, g, b = palette[color_idx:color_idx+3]
        else:
            if len(pixel) == 4:
                r, g, b, _ = pixel
            else:
                r, g, b = pixel
        return r, g, b

        
    def extract_frames(self):
        """
            Return ANSI dump of each frame in gif
        """
        if not self.is_gif():
            return []

        frame_list = []
        frame = Image.open(self.file_name)
        frames_created = 0
        while frame:
            ansi = self._get_gif_frame_ansi(frame)
            frames_created += 1
            clear(self.op_width, self.tsize.lines)
            sys.stdout.write(ansi)
            try:
                frame.seek(frames_created)
            except EOFError:
                break;
            frame_list.append(ansi)
        return frame_list


    
    
