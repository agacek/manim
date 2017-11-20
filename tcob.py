#!/usr/bin/env python

import math

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
from topics.vector_space_scene import LinearTransformationScene
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

def ceil(x):
    return int(math.ceil(x))

def floor(x):
    return int(math.floor(x))

class TrapezoidInequality(Scene):
    def construct(self):
        factor = 5.0
        self.add(NumberPlane(
            color=DARK_GREY,
            axes_color=GREY,
            secondary_line_ratio=factor-1
        ))
        def scale(n):
            return n / factor
        upper_y = 10
        lower_y = 3
        def upper_x(y):
            return 3 * y / 2.0
        def lower_x(y):
            return y / 2.0

        intro = TextMobject("""
            Consider the trapezoid: \\\\
            $3 \leq y \leq 10$ \\\\
            $y \leq 2x \leq 3y$
        """)
        intro.to_corner(UP+LEFT)
        intro.add_background_rectangle()
        self.play(Write(intro))
        self.dither(2)

        def fix_xy(p):
            x, y = p
            return (scale(x), scale(y), 0)
        def poly(*points, **kwargs):
            return Polygon(*map(fix_xy, points), **kwargs)

        p1 = (upper_x(lower_y), lower_y)
        p2 = (lower_x(lower_y), lower_y)
        p3 = (lower_x(upper_y), upper_y)
        p4 = (upper_x(upper_y), upper_y)
        trap = poly(p1, p2, p3, p4)
        self.play(Write(trap))
        self.dither(2)

        points = []
        for y in range(lower_y, upper_y + 1):
            for x in range(ceil(lower_x(y)), floor(upper_x(y)) + 1):
                points.append((x, y))

        A = [[1, 1], [1, 2]]
        A_inv = np.linalg.inv(A)

        def f(p):
            x, y, _ = p
            return (A_inv[0][0]*x + A_inv[0][1]*y, A_inv[1][0]*x + A_inv[1][1]*y, 0)

        def dot(pt, **kwargs):
            x, y = pt
            return Dot((scale(x), scale(y), 0), radius=0.04, **kwargs)

        def f_dot(pt):
            x, y = pt
            f_x, f_y, _ = f((x, y, 0))
            return Dot((scale(f_x), scale(f_y), 0), radius=0.04)

        def move(vm1, vm2):
            return Transform(vm1, vm2, run_time=DEFAULT_POINTWISE_FUNCTION_RUN_TIME)

        dots = [dot(pt) for pt in points]
        self.play(*map(Write, dots))
        self.dither(2)
        self.remove(intro)

        step2 = TextMobject("""
            Construct a transform relative to the lower bound on $x'$
        """)
        step2.to_edge(LEFT).to_edge(UP)
        step2.add_background_rectangle()
        self.play(Write(step2))
        self.dither(2)
        self.remove(step2)

        equations = TexMobject("""
            x &= x' + y' \\\\
            y &= x' + 2y' \\\\
            \\\\
            x' &= 2x - y  \\\\
            y' &= -x + y  \\\\
        """)
        equations.to_edge(LEFT).to_edge(UP)
        equations.add_background_rectangle()
        self.play(Write(equations))
        self.dither(2)

        dot_moves = [move(dt, f_dot(pt)) for dt, pt in zip(dots, points)]
        self.play(ApplyPointwiseFunction(f, trap), *dot_moves)

        self.dither(2)


        def tex(text):
            obj = TextMobject(text)
            obj.to_edge(DOWN)
            obj.add_background_rectangle()
            return obj


        obj = tex("""
            Original lower bound on $x$ is now {\em constant} lower bound on $x'$\\\\
            $y \leq 2x$ \\\\
            $x' + 2y' \leq 2x' + 2y'$ \\\\
            $0 \leq x'$
        """)
        self.play(Write(obj))
        self.dither()
        line = Line(f(fix_xy(p2)), f(fix_xy(p3)), color=GREEN)
        self.play(Indicate(line))
        self.remove(line)
        self.dither(4)
        self.remove(obj)

        obj = tex("""
            Original upper bound on $y$ is now upper bound on $x'$\\\\
            $y \leq 10$ \\\\
            $x' + 2y' \leq 10$ \\\\
            $x' \leq -2y' + 10$
        """)
        self.play(Write(obj))
        self.dither()
        line = Line(f(fix_xy(p3)), f(fix_xy(p4)), color=GREEN)
        self.play(Indicate(line))
        self.remove(line)
        self.dither(4)
        self.remove(obj)

        obj = tex("""
            Original upper bound on $x$ is now lower bound on $x'$\\\\
            $2x \leq 3y$ \\\\
            $2x' + 2y' \leq 3x' + 6y'$ \\\\
            $-4y' \leq x'$
        """)
        self.play(Write(obj))
        self.dither()
        line = Line(f(fix_xy(p4)), f(fix_xy(p1)), color=GREEN)
        self.play(Indicate(line))
        self.remove(line)
        self.dither(4)
        self.remove(obj)

        # Original lower bound on y is now lower bound on x'
        obj = tex("""
            Original upper bound on $y$ is now lower bound on $x'$\\\\
            $3 \leq y$ \\\\
            $3 \leq x' + 2y'$ \\\\
            $-2y' + 3 \leq x'$
        """)
        self.play(Write(obj))
        self.dither()
        line = Line(f(fix_xy(p1)), f(fix_xy(p2)), color=GREEN)
        self.play(Indicate(line))
        self.remove(line)
        self.dither(4)
        self.remove(obj)

        self.dither()

        obj = tex("""
            Reduction then depends on the original solution $v$\\\\
            Here are the cases
        """)
        self.play(Write(obj))
        self.dither(2)

        color = DARK_BLUE
        v = dot((1, 3), color=color)
        self.play(FocusOn(v))
        self.add(v)
        self.dither()
        s1 = (0, 5)
        s2 = (0, 1.5)
        s3 = (7, 1.5)
        sub = poly(s1, s2, s3, color=color)
        self.play(Write(sub))
        self.dither(2)
        self.remove(v)
        self.remove(sub)

        v = dot((6, 0), color=color)
        self.play(FocusOn(v))
        self.add(v)
        self.dither()
        s1 = (0, 1.5)
        s2 = (7, 1.5)
        s3 = (13, -1.5)
        s4 = (6, -1.5)
        sub = poly(s1, s2, s3, s4, color=color)
        self.play(Write(sub))
        self.dither(2)
        self.remove(v)
        self.remove(sub)

        v = dot((14, -3), color=color)
        self.play(FocusOn(v))
        self.add(v)
        self.dither()
        s1 = (6, -1.5)
        s2 = (13, -1.5)
        s3 = (20, -5)
        sub = poly(s1, s2, s3, color=color)
        self.play(Write(sub))
        self.dither(2)
        self.remove(v)
        self.remove(sub)

        self.remove(obj)
        self.dither(5)
        

class ThinInequality(Scene):
    def construct(self):
        factor = 5.0
        self.add(NumberPlane(
            color=DARK_GREY,
            axes_color=GREY,
            secondary_line_ratio=factor-1
        ))
        def scale(n):
            return n / factor
        upper_y = 12
        lower_y = 0
        def upper_x(y):
            return (y + 3) / 3.0
        def lower_x(y):
            return 2 * y / 5.0

        intro = TextMobject("""
            Consider the trapezoid: \\\\
            $0 \leq y \leq 12$ \\\\
            $2y \leq 5x \land 3x \leq y+3$
        """)
        intro.to_corner(UP+LEFT)
        intro.add_background_rectangle()
        self.play(Write(intro))
        self.dither()

        def fix_xy(p):
            x, y = p
            return (scale(x), scale(y), 0)
        def poly(*points, **kwargs):
            return Polygon(*map(fix_xy, points), **kwargs)

        p1 = (upper_x(lower_y), lower_y)
        p2 = (lower_x(lower_y), lower_y)
        p3 = (lower_x(upper_y), upper_y)
        p4 = (upper_x(upper_y), upper_y)
        trap = poly(p1, p2, p3, p4)
        self.play(Write(trap))
        self.dither()

        points = []
        for y in range(lower_y, upper_y + 1):
            for x in range(ceil(lower_x(y)), floor(upper_x(y)) + 1):
                points.append((x, y))

        A = [[1, 2], [2, 5]]
        A_inv = np.linalg.inv(A)

        def f(p):
            x, y, _ = p
            return (A_inv[0][0]*x + A_inv[0][1]*y, A_inv[1][0]*x + A_inv[1][1]*y, 0)

        def dot(pt, **kwargs):
            x, y = pt
            return Dot((scale(x), scale(y), 0), radius=0.04, **kwargs)

        def f_dot(pt):
            x, y = pt
            f_x, f_y, _ = f((x, y, 0))
            return Dot((scale(f_x), scale(f_y), 0), radius=0.04)

        def move(vm1, vm2):
            return Transform(vm1, vm2, run_time=DEFAULT_POINTWISE_FUNCTION_RUN_TIME)

        dots = [dot(pt) for pt in points]
        self.play(*map(Indicate, dots))
        self.dither(2)
        self.remove(intro)

        problem = TextMobject("""
            Some values for $y$ have no solutions for $x$
        """)
        problem.to_corner(UP+LEFT)
        problem.add_background_rectangle()
        self.play(Write(problem))
        self.dither()
        for y in 8, 11:
            line = Line((scale(lower_x(y)), scale(y), 0), (scale(upper_x(y)), scale(y), 0), color=RED)
            self.play(FocusOn(line))
            self.add(line)
            self.dither()
            self.remove(line)
        self.dither(2)
        self.remove(problem)

        step2 = TextMobject("""
            Construct a transform relative to the lower bound on $x'$
        """)
        step2.to_edge(LEFT).to_edge(UP)
        step2.add_background_rectangle()
        self.play(Write(step2))
        self.dither(2)
        self.remove(step2)

        equations = TexMobject("""
            x &= x' + 2y' \\\\
            y &= 2x' + 5y' \\\\
            \\\\
            x' &= 5x - 2y  \\\\
            y' &= -2x + y  \\\\
        """)
        equations.to_edge(LEFT).to_edge(UP)
        equations.add_background_rectangle()
        self.play(Write(equations))
        self.dither(2)

        dot_moves = [move(dt, f_dot(pt)) for dt, pt in zip(dots, points)]
        self.play(ApplyPointwiseFunction(f, trap), *dot_moves)

        self.dither(2)

        self.remove(equations)
        for mob in self.get_mobjects():
            mob.target = mob.copy().scale(3)
        self.play(*[
            Transform(mob, mob.target)
            for mob in self.get_mobjects()
        ])
        self.add(equations)

        self.dither(5)
        
class ThinInequalityMulti(Scene):
    def construct(self):
        def example(r, s):
            factor = 5.0
            self.add(NumberPlane(
                color=DARK_GREY,
                axes_color=GREY,
                secondary_line_ratio=factor-1
            ))
            def scale(n):
                return n / factor
            upper_y = 12
            lower_y = 0
            def upper_x(y):
                return (y + 3) / 3.0
            def lower_x(y):
                return 2 * y / 5.0

            def fix_xy(p):
                x, y = p
                return (scale(x), scale(y), 0)
            def poly(*points, **kwargs):
                return Polygon(*map(fix_xy, points), **kwargs)

            p1 = (upper_x(lower_y), lower_y)
            p2 = (lower_x(lower_y), lower_y)
            p3 = (lower_x(upper_y), upper_y)
            p4 = (upper_x(upper_y), upper_y)
            trap = poly(p1, p2, p3, p4)
            self.add(trap)

            points = []
            for y in range(lower_y, upper_y + 1):
                for x in range(ceil(lower_x(y)), floor(upper_x(y)) + 1):
                    points.append((x, y))

            A = [[r, 2],
                 [s, 5]]
            A_inv = np.linalg.inv(A)

            tex = TexMobject("""
                M &= \\left(\\begin{{matrix}} {0} & {1} \\\\ {2} & {3} \\end{{matrix}}\\right)
            """.format(A[0][0], A[0][1], A[1][0], A[1][1]))
            tex.to_corner(UP+LEFT)
            tex.add_background_rectangle()
            self.add(tex)

            def f(p):
                x, y, _ = p
                return (A_inv[0][0]*x + A_inv[0][1]*y, A_inv[1][0]*x + A_inv[1][1]*y, 0)

            def dot(pt, **kwargs):
                x, y = pt
                return Dot((scale(x), scale(y), 0), radius=0.04, **kwargs)

            def f_dot(pt):
                x, y = pt
                f_x, f_y, _ = f((x, y, 0))
                return Dot((scale(f_x), scale(f_y), 0), radius=0.04)

            def move(vm1, vm2):
                return Transform(vm1, vm2, run_time=DEFAULT_POINTWISE_FUNCTION_RUN_TIME)

            dots = [dot(pt) for pt in points]
            self.add(*dots)

            self.dither(1)
            dot_moves = [move(dt, f_dot(pt)) for dt, pt in zip(dots, points)]
            self.play(ApplyPointwiseFunction(f, trap), *dot_moves)

            self.dither(1)

            self.remove(tex)
            for mob in self.get_mobjects():
                mob.target = mob.copy().scale(2)
            self.play(*[
                Transform(mob, mob.target)
                for mob in self.get_mobjects()
            ])
            self.add(tex)
            self.dither(3)
            self.remove(*self.get_mobjects())

        # example(r, s) must have 5r - 2s = 1
        example(1, 2)
        example(3, 7)
        example(5, 12)
        example(7, 17)
        example(21, 52)
        example(-1, -3)
        example(-3, -8)
        example(-5, -13)
