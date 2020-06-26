from moviepy.editor import ImageSequenceClip
import numpy as np

def display_via_moviepy(images, title):
    """Display an animated sequence of images in the browser using moviepy."""
    as_arrays = [np.array(image) for image in images]
    return ImageSequenceClip(as_arrays, fps=24).ipython_display()
