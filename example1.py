#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 16:02:59 2020

@author: gutin
"""

from laguerre_transformations import *

circle1 = make_circle((100,100),100,nlines=50)
circle2 = make_circle((50,50),-100,nlines=50)

transformation = dual_matrix(3,5,-1,3,9,-6,4,2)

animate_transformation(transformation,
                       circle1 + circle2,
                       "transformation_animation.gif",
                       offset=(200,200))