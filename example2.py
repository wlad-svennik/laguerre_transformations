#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 16:02:59 2020

@author: gutin
"""

from laguerre_transformations import *

grid = make_grid()

transformation = dual_matrix(3,5,-1,3,9,-6,4,2)

animate_transformation(transformation,
                       grid,
                       width=5,
                       offset=(200,200))