# Laguerre transformations

Python code for visualising Laguerre transformations of oriented lines in the Euclidean plane.

Like Möbius transformations, these can be represented by 2×2 matrices. Here the entries are dual numbers. Circles are represented by their oriented tangent lines, so their images can be drawn by transforming those lines.

## Examples

```python
from laguerre_transformations import (
    animate_transformation,
    dual_matrix,
    make_circle,
    make_grid,
)

circle1 = make_circle((100, 100), 100)
circle2 = make_circle((50, 50), -100)
transformation = dual_matrix(3, 5, -1, 3, 9, -6, 4, 2)

animation = animate_transformation(
    transformation,
    circle1 + circle2,
    offset=(200, 200),
)
```

This interpolates from the identity towards the given transformation and animates its effect on two circles.

![Two circles undergoing a Laguerre transformation](examples/two_circles.gif)

The same transformation can be applied to a square grid:

```python
animation = animate_transformation(
    transformation,
    make_grid(),
    offset=(200, 200),
)
```

![A grid undergoing a Laguerre transformation](examples/grid.gif)

## Installation

Requires Python 3 with Tk support. To install from this repository:

```sh
git clone https://github.com/wlad-svennik/laguerre_transformations.git
cd laguerre_transformations
python -m pip install .
```

The package is also published on [PyPI](https://pypi.org/project/laguerre-transformations/):

```sh
python -m pip install laguerre_transformations
```

## Background

See [Laguerre transformations on Wikipedia](https://en.wikipedia.org/wiki/Laguerre_transformations) for the mathematical background and [hyperbolic_laguerre_transformations](https://github.com/wlad-svennik/hyperbolic_laguerre_transformations) for the related construction over the split-complex numbers.

The code is available under the [BSD 3-Clause licence](LICENSE.txt).

