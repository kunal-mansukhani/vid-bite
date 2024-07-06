from manim import *

class DashedLineExample(Scene):
    def construct(self):
        # dash_length increased
        dashed_1 = DashedLine(config.left_side, config.right_side, dash_length=2.0).shift(UP*2)
        # normal
        dashed_2 = DashedLine(config.left_side, config.right_side)
        # dashed_ratio decreased
        dashed_3 = DashedLine(config.left_side, config.right_side, dashed_ratio=0.1).shift(DOWN*2)
        self.add(dashed_1, dashed_2, dashed_3)