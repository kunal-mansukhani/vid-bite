from manim import *

class RectangleExample(Scene):
    def construct(self):
        rect1 = Rectangle(width=4.0, height=2.0, grid_xstep=1.0, grid_ystep=0.5)
        rect2 = Rectangle(width=1.0, height=4.0)
        rect3 = Rectangle(width=2.0, height=2.0, grid_xstep=1.0, grid_ystep=1.0)
        rect3.grid_lines.set_stroke(width=1)

        rects = Group(rect1, rect2, rect3).arrange(buff=1)
        self.add(rects)