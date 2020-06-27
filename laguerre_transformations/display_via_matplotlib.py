def display_via_matplotlib(images, title):
    """Display an animated sequence of images using Matplotlib."""
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation

    fig = plt.figure(figsize=(images[0].width/100,images[1].height/100))
    ims = []
    for i in range(len(images)):
        im = plt.imshow(images[i], animated=True)
        ims.append([im])
    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                    repeat_delay=0)
    plt.axis('off')    
    plt.axis("tight")
    plt.axis("image")
    fig.tight_layout(pad=0)
    if title is not None:
        fig.canvas.set_window_title(title)
    plt.show()
    return ani
