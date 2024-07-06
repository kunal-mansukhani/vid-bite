from manim import *

class ScaleInPlaceExample(Scene):
    def construct(self):
        self.play(ScaleInPlace(Text("Hello World!"), 2))