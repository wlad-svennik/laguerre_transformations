#!/bin/python

from mttkinter import mtTkinter as tk
from itertools import count
from PIL import ImageTk
from tkinter.filedialog import asksaveasfilename
import tkinter.font as font
from threading import Thread
import pickle
import sys
import subprocess

""" The `display` function displays a sequence of images as an animation
with a given title.
A major goal of this file is to allow an animation to be displayed without
blocking the terminal. Ideally, this would be achieved by launching Tkinter
in a separate thread. Unfortunately, that idea doesn't work because Tkinter
doesn't play well with multiple threads. So to get around the problem,
we launch Tkinter in a separate process, not a separate thread."""

def display(images, title):
    """Display an animated sequence of images in a new window and proces."""
    # We launch the new process inside a new thread because subprocess.run
    # is blocking
    Thread(target=lambda:
        subprocess.run(['python',__file__],
                       input=pickle.dumps((images,title)))).start()
    
def main(images, title):
    root = tk.Tk()
    if title is not None:
        root.title(title)
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Save As...",
                         command=lambda: save_animation(images))
    menubar.add_cascade(label="File", menu=filemenu)
    lbl = ImageLabel(root)
    lbl.pack()
    lbl.load(images)
    lbl.configure(background='black')
    #root.configure(background='gray')
    pause_play = tk.Button(root,
                           text="⏯️",
                           font=font.Font(size=30),
                           command=lambda: lbl.pause_play())
    pause_play.pack(expand=True, fill=tk.X, side=tk.RIGHT)
    root.config(menu=menubar)
    root.mainloop()

class ImageLabel(tk.Label):
    """A label that displays images, and plays them if there are more
    than one."""
    def load(self, im):
        self.loc = 0
        self.frames = []
        self.paused = False
        try:
            for i in count(0):
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

def save_animation(images):
    """Saves an animation (usually as a GIF)."""
    ftypes = [('GIF file', '.gif'),
              ('All files', '*')]
    filename = asksaveasfilename(filetypes=ftypes, defaultextension='.gif')
    if filename != () and filename != '':
        images[0].save(filename, save_all=True, loop=0,
              append_images = images[1:])

if __name__ == "__main__":
    images, title = pickle.loads(sys.stdin.buffer.read())
    main(images, title)