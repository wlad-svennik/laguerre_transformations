import tkinter as tk
from itertools import count
from PIL import ImageTk

class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        self.loc = 0
        self.frames = []
        self.paused = False
        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im[i]))
        except IndexError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 50
        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()
            
    def pause_play(self):
        self.paused = not self.paused
        self.next_frame()
        
    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames and not self.paused:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)