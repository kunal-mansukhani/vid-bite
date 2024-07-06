from manim import *

class CircleExample(Scene):
    def construct(self):
        circle_1 = Circle(radius=1.0)
        circle_2 = Circle(radius=1.5, color=GREEN)
        circle_3 = Circle(radius=1.0, color=BLUE_B, fill_opacity=1)

        circle_group = Group(circle_1, circle_2, circle_3).arrange(buff=1)
        self.add(circle_group)