from manim import *

class AnimatedBoundaryExample(Scene):
    def construct(self):
        text = Text("So shiny!")
        boundary = AnimatedBoundary(text, colors=[RED, GREEN, BLUE],
                                    cycle_rate=3)
        self.add(text, boundary)
        self.wait(2)