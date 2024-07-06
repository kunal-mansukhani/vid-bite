from manim import *

class FadeToColorExample(Scene):
    def construct(self):
        self.play(FadeToColor(Text("Hello World!"), color=RED))