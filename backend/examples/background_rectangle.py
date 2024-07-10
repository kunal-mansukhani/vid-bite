from manim import *

class ExampleBackgroundRectangle(Scene):
    def construct(self):
        circle = Circle().shift(LEFT)
        circle.set_stroke(color=GREEN, width=20)
        triangle = Triangle().shift(2 * RIGHT)
        triangle.set_fill(PINK, opacity=0.5)
        backgroundRectangle1 = BackgroundRectangle(circle, color=WHITE, fill_opacity=0.15)
        backgroundRectangle2 = BackgroundRectangle(triangle, color=WHITE, fill_opacity=0.15)
        self.add(backgroundRectangle1)
        self.add(backgroundRectangle2)
        self.add(circle)
        self.add(triangle)
        self.play(Rotate(backgroundRectangle1, PI / 4))
        self.play(Rotate(backgroundRectangle2, PI / 2))