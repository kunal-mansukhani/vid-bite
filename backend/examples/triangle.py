from manim import *

class TriangleExample(Scene):
    def construct(self):
        triangle_1 = Triangle()
        triangle_2 = Triangle().scale(2).rotate(60*DEGREES)
        tri_group = Group(triangle_1, triangle_2).arrange(buff=1)
        self.add(tri_group)
