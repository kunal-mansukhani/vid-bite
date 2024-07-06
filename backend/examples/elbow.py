from manim import *

class ElbowExample(Scene):
    def construct(self):
        elbow_1 = Elbow()
        elbow_2 = Elbow(width=2.0)
        elbow_3 = Elbow(width=2.0, angle=5*PI/4)

        elbow_group = Group(elbow_1, elbow_2, elbow_3).arrange(buff=1)
        self.add(elbow_group)