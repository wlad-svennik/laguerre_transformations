import tkinter as tk
from itertools import count
from PIL import ImageTk
from tkinter.filedialog import asksaveasfilename
import tkinter.font as font
from multiprocessing import Process
    
def display_tk_multiprocess(images, title):
    Process(target=do_display_tk_multiprocess, args=(images,title)).start()

def do_display_tk_multiprocess(images, title):
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
        
