def display_via_videofig(images, title):
    """Display an animated sequence of images in a new window."""
    from videofig import videofig
    # redraw_fn draw frame f in a image sequence
    def redraw_fn(i, axes):
        if not redraw_fn.initialized:
            redraw_fn.im = axes.imshow(images[i], animated=True)
            redraw_fn.initialized = True
        else:
            redraw_fn.im.set_array(images[i])
    redraw_fn.initialized = False
    return videofig(len(images), redraw_fn, play_fps=30)
