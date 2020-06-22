#!/usr/bin/env python3

from PIL import Image, ImageDraw
from sympy import *
from sympy.abc import *
from sympy import pi

one = eye(2)
eps = Matrix([[0,1],[0,0]])

def dual_number(a,b):
    return a*one + b*eps

def dual_ratio(a,b,c,d):
    return Matrix([dual_number(a,b),
                   dual_number(c,d)])

def dual_matrix(A,B,C,D,E,F,G,H):
    return Matrix([
        [A*one+B*eps,C*one+D*eps],
        [E*one+F*eps,G*one+H*eps]])

def make_line(theta, R):
    """Generates a dual number ratio that represents a line, where
    theta is the angle made with the x-axis, and R is the perpendicular
    distance from the origin."""
    return dual_ratio(sin(theta/2),R*cos(theta/2)/2,
                      cos(theta/2),-R*sin(theta/2)/2)

def sqrt_dual_number(dual):
    """Takes the square root of a dual number."""
    a, b = dual[0,0], dual[0,1]
    return Matrix([[sqrt(a), b/(2*sqrt(a))], [0, sqrt(a)]])

def normalisation_constant(dr):
    return sqrt_dual_number(dr[0:2,:]**2 + dr[2:4,:]**2)

def get_line(dr):
    """Returns the (theta, R) values of a line 'dr' where theta is the angle
    with the x-axis and R is the perpendicular distance from the origin."""
    # Do the following line twice, because otherwise it somehow fails to
    # normalise it some of the time
    dr = dr * normalisation_constant(dr).inv()
    dr = dr * normalisation_constant(dr).inv()
    theta = 2*atan2(dr[0,0],dr[2,0])
    abs_R = sqrt(dr[0,1] ** 2 + dr[2,1] ** 2) / sqrt(dr[0,0] ** 2 + dr[2,0] ** 2) * 2
    sign_R = Piecewise((sign(dr[0,1] * dr[2,0]), sin(theta/2)**2 < Integer(1)/2),
                       (-sign(dr[0,0] * dr[2,1]), True))
    return theta, abs_R * sign_R

def translation(x,y):
    """Returns a matrix that represents a translation as a Laguerre
    transformation."""
    return dual_matrix(1,x, 0,y,
                       0,y, 1,-x)

def make_circle(centre, radius, nlines=100):
    """Returns a list of lines (as dual number ratios) which are tangent
    to a circle of given centre and radius."""
    cx, cy = centre
    return [translation(cx,cy) * make_line(2*i*pi/nlines, radius)
            for i in range(0,nlines)]

def make_grid(nlines=100, spacing=100):
    """Return a list of lines (as dual numbers) which make up a square grid"""
    horizontal_lines = [make_line(0,spacing*i) for i in range(-nlines//4, nlines//4)]
    vertical_lines   = [make_line(pi/2,spacing*i) for i in range(-nlines//4, nlines//4)]
    return horizontal_lines + vertical_lines

def dilatation(t):
    """Returns a matrix that represents an axial dilatation."""
    return Matrix([[one,t*eps/2],[-t*eps/2,one]])

def interpolate(transformation, nframes=50):
    """Returns a list of transformations that interpolates between the
    identity transformation and the specified transformation. If 'nframes'
    equals 1, then simply return the input transformation in a singleton
    list."""
    if nframes == 1:
        return [transformation]
    transformation = MutableMatrix(transformation)
    print('Taking logarithm of transformation...')
    log_transformation = simplify(transformation.analytic_func(log(x),x))
    print('Generating intermediate transformations...')
    return [re(simplify(exp(log_transformation.evalf() * i/nframes)))
            for i in range(nframes)]

def rotation(theta):
    """Returns a matrix that represents a rotation about the origin
    as a Laguerre transformation."""
    return Matrix([[cos(theta/2)*one,-sin(theta/2)*one],
                    [sin(theta/2)*one,cos(theta/2)*one]])

def apply_transformations(transformations, lines):
    """Applies a list of transformations to a list of lines, generating
    a list of 'frames'. A 'frame' in this case is a list of lines
    each represented as a dual number ratio."""
    frames = []
    nframes= len(transformations)
    for i in range(nframes):
        frames.append([])
        print('Applying transformation', i, '...')
        transformation = transformations[i]
        for line in lines:
            frames[-1].append((transformation * line).evalf())
    return frames

def draw_frames(frames, imgx=900, imgy=900, offset=(0,0), width=1):
    """Returns a list of images which together make up an animation."""
    offsetting_translation = translation(*offset)
    nframes = len(frames)
    images = [Image.new("RGB", (imgx, imgy)) for i in range(nframes)]
    for i in range(len(frames)):
        print('Drawing frame', i, '...')
        draw = ImageDraw.Draw(images[i])
        for line in frames[i]:
            theta, R = get_line(offsetting_translation * line)
            if cos(theta)**2 > 1/2:
                draw.line((0,R/cos(theta),imgx,R/cos(theta) - imgx*tan(theta)),
                          width=width, fill=128)
            else:
                draw.line((R/sin(theta),0,R/sin(theta) - imgy*cot(theta),imgy),
                          width=width, fill=128)
    return images

def save_animation(images, filename):
    """Saves an animation (usually as a GIF)."""
    images[0].save(filename, save_all=True, loop=0,
          append_images = images[1:])

def animate_transformation(transformation,
                           lines,
                           filename,
                           nframes=50,
                           offset=(0,0),
                           width=1):
    """Takes as input a transformation, a list of lines, and a filename.
    It interpolates the transformation starting from the identity
    transformation. It then animates the result of applying the sequence
    of interpolated transformations to each line, and saves the result to the
    specified file."""
    intermediate_transformations = interpolate(transformation, nframes=nframes)
    frames = apply_transformations(intermediate_transformations, lines)
    images = draw_frames(frames, offset=offset, width=width)
    save_animation(images, filename)