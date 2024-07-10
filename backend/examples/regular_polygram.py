from manim import *

class RegularPolygramExample(Scene):
    def construct(self):
        pentagram = RegularPolygram(5, radius=2)
        self.add(pentagram)