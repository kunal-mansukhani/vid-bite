from manim import *

class RightAngleExample(Scene):
    def construct(self):
        line1 = Line( LEFT, RIGHT )
        line2 = Line( DOWN, UP )
        rightangles = [
            RightAngle(line1, line2),
            RightAngle(line1, line2, length=0.4, quadrant=(1,-1)),
            RightAngle(line1, line2, length=0.5, quadrant=(-1,1), stroke_width=8),
            RightAngle(line1, line2, length=0.7, quadrant=(-1,-1), color=RED),
        ]
        plots = VGroup()
        for rightangle in rightangles:
            plot=VGroup(line1.copy(),line2.copy(), rightangle)
            plots.add(plot)
        plots.arrange(buff=1.5)
        self.add(plots)