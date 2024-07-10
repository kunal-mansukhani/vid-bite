from manim import *

class LabeledArrowExample(Scene):
    def construct(self):
        l_arrow = LabeledArrow("0.5", start=LEFT*3, end=RIGHT*3 + UP*2, label_position=0.5)

        self.add(l_arrow)