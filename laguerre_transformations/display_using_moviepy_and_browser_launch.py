def display_using_moviepy_and_browser_launch(images, title):
    """Display an animated sequence of images in the browser using moviepy."""
    from moviepy.editor import ImageSequenceClip
    import numpy as np
    import webbrowser
    import tempfile
    from time import sleep
    as_arrays = [np.array(image) for image in images]
    the_html = ImageSequenceClip(as_arrays, fps=24).ipython_display()
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.html') as f:
        f.write(the_html.data)
        webbrowser.open(f.name)
        # This is to allow the browser time to open the file before it gets destroyed
        # It's a hack
        sleep(1)