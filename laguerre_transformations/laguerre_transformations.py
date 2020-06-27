from PIL import Image, ImageDraw
from numpy import eye, block, sin, cos, tan, arctan2, sign, array, pi
from scipy.linalg import logm, expm
try:
    from .display import display
except ImportError:
    from display import display

one = eye(2)
eps = array([[0,1],[0,0]])

def dual_number(a,b):
    """Uses a 2x2 matrix to represent a dual number."""
    return a*one + b*eps

def dual_ratio(a,b,c,d):
    """Uses a 4x2 matrix to represent a pair of dual numbers, understood
    as a point on the projective dual line."""
    return block([[dual_number(a,b)],
                  [dual_number(c,d)]])

def dual_matrix(A,B,C,D,E,F,G,H):
    """Uses a 4x4 matrix to represent a 2x2 matrix of dual numbers."""
    return block([
        [A*one+B*eps,C*one+D*eps],
        [E*one+F*eps,G*one+H*eps]])

def make_line(theta, R):
    """Generates a dual number ratio that represents a line, where
    theta is the angle made with the x-axis, and R is the perpendicular
    distance from the origin."""
    return dual_ratio(sin(theta/2),R*cos(theta/2)/2,
                      cos(theta/2),-R*sin(theta/2)/2)

def inv_sqrt_dual_number(dual):
    """Takes one over the square root of a dual number."""
    a, b = dual[0,0], dual[0,1]
    inv_sqrt_a = a**-0.5
    return array([[inv_sqrt_a, -b*inv_sqrt_a/(2*a)], [0, inv_sqrt_a]])

def squared(mat):
    """Multiplies a matrix by itself."""
    return mat @ mat

def normalise(dr):
    """Normalises a dual number ratio [a:b] to [a':b'] such that
    (a')**2 + (b')**2 == 1"""
    normalisation_constant = inv_sqrt_dual_number(squared(dr[0:2,:]) +
                                                  squared(dr[2:4,:]))
    return dr @ normalisation_constant

def get_line(dr):
    """Returns the (theta, R) values of a line 'dr' where theta is the angle
    with the x-axis and R is the perpendicular distance from the origin."""
    # Do the following line twice, because otherwise it somehow fails to
    # normalise it some of the time
    dr = normalise(dr)
    theta = 2*arctan2(float(dr[0,0]),float(dr[2,0]))
    abs_R = (dr[0,1]**2 + dr[2,1]**2)**0.5 * (dr[0,0]**2 + dr[2,0]**2)**-0.5 * 2
    sign_R = (sign(dr[0,1] * dr[2,0]) * (sin(theta/2)**2 < 1/2)) +\
        (-sign(dr[0,0] * dr[2,1]) * (sin(theta/2)**2 >= 1/2))
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
    return [translation(cx,cy) @ make_line(2*i*pi/nlines, radius)
            for i in range(0,nlines)]

def make_grid(nlines=100, spacing=100):
    """Return a list of lines (as dual numbers) which make up a square grid"""
    horizontal_lines = [make_line(0,spacing*i) for i in range(-nlines//4, nlines//4)]
    vertical_lines   = [make_line(pi/2,spacing*i) for i in range(-nlines//4, nlines//4)]
    return horizontal_lines + vertical_lines

def dilatation(t):
    """Returns a matrix that represents an axial dilatation."""
    return block([[one,t*eps/2],[-t*eps/2,one]])

def dual_matrix_determinant(m):
    a = m[0:2,0:2]
    b = m[0:2,2:4]
    c = m[2:4,0:2]
    d = m[2:4,2:4]
    return a @ d  - b @ c

class DeterminantNegativeException(Exception):
    pass

def interpolate(transformation, nframes=50):
    """Returns a list of transformations that interpolates between the
    identity transformation and the specified transformation. If 'nframes'
    equals 1, then simply return the input transformation in a singleton
    list."""
    if nframes == 1:
        return [transformation]
    if dual_matrix_determinant(transformation)[0,0] <= 0:
        raise DeterminantNegativeException
    log_transformation = logm(transformation)
    return [expm(log_transformation * i/nframes).real
            for i in range(nframes)]

def rotation(theta):
    """Returns a matrix that represents a rotation about the origin
    as a Laguerre transformation."""
    return block([[cos(theta/2)*one,-sin(theta/2)*one],
                    [sin(theta/2)*one,cos(theta/2)*one]])

def rotation_about_centre(centre, theta):
    """Returns a matrix that represents a rotation about the given centre
    as a Laguerre transformation"""
    return translation(*centre) @ rotation(theta) @ translation(-centre[0],-centre[1])

def apply_transformations(transformations, lines):
    """Applies a list of transformations to a list of lines, generating
    a list of 'frames'. A 'frame' in this case is a list of lines
    each represented as a dual number ratio."""
    frames = []
    nframes= len(transformations)
    for i in range(nframes):
        frames.append([])
        transformation = transformations[i]
        for line in lines:
            frames[-1].append(transformation @ line)
    return frames

def draw_frames(frames, imgx=900, imgy=900, offset=(0,0), width=1):
    """Returns a list of images which together make up an animation."""
    offsetting_translation = translation(*offset)
    nframes = len(frames)
    images = [Image.new("RGB", (imgx, imgy)) for i in range(nframes)]
    for i in range(len(frames)):
        draw = ImageDraw.Draw(images[i])
        for line in frames[i]:
            theta, R = get_line(offsetting_translation @ line)
            if cos(theta)**2 > 1/2:
                draw.line((0,R/cos(theta),imgx,R/cos(theta) - imgx*tan(theta)),
                          width=width, fill=128)
            else:
                draw.line((R/sin(theta),0,R/sin(theta) - imgy*tan(pi/2 - theta),imgy),
                          width=width, fill=128)
    return images

def animate_transformation_without_display(transformation,
                                           lines,
                                           nframes=100,
                                           offset=(0,0),
                                           width=1,
                                           title=None):
    try:
        intermediate_transformations = interpolate(transformation, nframes=nframes)
    except DeterminantNegativeException:
        print("Determinant of the input matrix is negative. Call instead with nframes=1.")
        print("Note that this determinant is dual-number valued.")
        return
    frames = apply_transformations(intermediate_transformations, lines)
    images = draw_frames(frames, offset=offset, width=width)
    return images


def animate_transformation(transformation,
                           lines,
                           nframes=100,
                           offset=(0,0),
                           width=1,
                           title=None,
                           via='matplotlib'):
    """Takes as input a transformation and a list of lines.
    It interpolates the transformation starting from the identity
    transformation. It then animates the result of applying the sequence
    of interpolated transformations to each line, and displays the result."""
    try:
        intermediate_transformations = interpolate(transformation, nframes=nframes)
    except DeterminantNegativeException:
        print("Determinant of the input matrix is negative. Call instead with nframes=1.")
        print("Note that this determinant is dual-number valued.")
        return
    frames = apply_transformations(intermediate_transformations, lines)
    images = draw_frames(frames, offset=offset, width=width)
    return display(images, title, via=via)