#!/usr/bin/env python

from helpers import *

from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import *

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from animation.playground import *
from topics.geometry import *
from topics.characters import *
from topics.functions import *
from topics.number_line import *
from topics.combinatorics import *
from scene import Scene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *

from mobject.vectorized_mobject import *

## To watch one of these scenes, run the following:
## python extract_scenes.py -p file_name <SceneName>

def f(p):
    x, y, z = p
    #return ((x + y + 1) / 2.0, y, 0)
    return (x / 2.0, (y - 1) / 2.0, 0)

# x = 2*x'
# y = 2*y' + 1
#
#
# [[2 0]    [0
#  [0 2]] +  1]
# y - 1

def tcob(t):
    return ApplyPointwiseFunction(f, t)

def pt_tcob(x, y):
    return Transform(pt(x, y), f_pt(x, y), run_time=DEFAULT_POINTWISE_FUNCTION_RUN_TIME)

def pt(x, y):
    return Dot((x, y, 0), color=GREEN, radius=0.1)

def f_pt(x, y):
    return Dot(f((x, y, 0)), color=GREEN, radius=0.1)

class WholeGrid(Scene):
    def construct(self):
        square = Square()
        self.add(NumberPlane(
            color=DARK_GREY,
            axes_color=GREY,
            secondary_line_ratio=0
        ))
        points = []
        points_transform = []
        for x in range(-10, 10):
            for y in range(-10, 10):
                points.append(pt(x, y))
                points_transform.append(pt_tcob(x, y))

        self.add(*points)
        self.dither(1)
        self.remove( *points)
        self.play(*points_transform)
        self.dither(1)

class TwoTrapezoids(Scene):
    def construct(self):
        square = Square()
        self.add(NumberPlane(
            color=DARK_GREY,
            axes_color=GREY,
            secondary_line_ratio=0
        ))
        t1 = Polygon(
            (0, 3, 0),
            (2, 1, 0),
            (4, 1, 0),
            (5, 3, 0)
        )
        t2 = Polygon(
            (-2, -1, 0),
            (-4, -3, 0),
            (2, -3, 0),
            (1, -1, 0)
        )
        points = []
        points_transform = []
        missed = []
        for x, y in ([(0, 3), (1, 2), (2, 1), (2, 3), (3, 2), (4, 1), (4, 3)] +
                     [(-4, -3), (-3, -2), (-2, -3), (-2, -1), (-1, -2), (0, -3), (0, -1), (1, -2), (2, -3)]):
            p = pt(x, y)
            fp = f_pt(x, y)
            points.append(p)
            if x % 2 != 0:
                missed.append(fp)
            points_transform.append(Transform(p, fp, run_time=DEFAULT_POINTWISE_FUNCTION_RUN_TIME))

        self.add(t1, t2, *points)
        self.dither(2)
        self.remove(t1, t2, *points)
        self.play(tcob(t1), tcob(t2), *points_transform, replace_mobject_with_target_in_scene=True)
        self.dither(1)

        self.remove(VGroup(*missed))
        self.play(FadeOut(VGroup(*missed)))
        self.dither(2)
