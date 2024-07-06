from manim import *

class PointFromProportion(Scene):
    def construct(self):
        line = Line(2*DL, 2*UR)
        self.add(line)
        colors = (RED, BLUE, YELLOW)
        proportions = (1/4, 1/2, 3/4)
        for color, proportion in zip(colors, proportions):
            self.add(Dot(color=color).move_to(
                    line.point_from_proportion(proportion)
            ))