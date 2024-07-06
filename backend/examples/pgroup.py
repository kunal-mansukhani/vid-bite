from manim import *

class PgroupExample(Scene):
    def construct(self):

        p1 = PointCloudDot(radius=1, density=20, color=BLUE)
        p1.move_to(4.5 * LEFT)
        p2 = PointCloudDot()
        p3 = PointCloudDot(radius=1.5, stroke_width=2.5, color=PINK)
        p3.move_to(4.5 * RIGHT)
        pList = PGroup(p1, p2, p3)

        self.add(pList)