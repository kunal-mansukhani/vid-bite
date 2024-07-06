
from manim import *

class ShowWrite(Scene):
    def construct(self):
        self.play(Write(Text("Hello", font_size=144)))