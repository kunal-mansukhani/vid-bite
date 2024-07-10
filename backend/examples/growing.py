from manim import *

class Growing(Scene):
    def construct(self):
        square = Square()
        circle = Circle()
        triangle = Triangle()
        arrow = Arrow(LEFT, RIGHT)
        star = Star()

        VGroup(square, circle, triangle).set_x(0).arrange(buff=1.5).set_y(2)
        VGroup(arrow, star).move_to(DOWN).set_x(0).arrange(buff=1.5).set_y(-2)

        self.play(GrowFromPoint(square, ORIGIN))
        self.play(GrowFromCenter(circle))
        self.play(GrowFromEdge(triangle, DOWN))
        self.play(GrowArrow(arrow))
        self.play(SpinInFromNothing(star))

class GrowArrowExample(Scene):
    def construct(self):
        arrows = [Arrow(2 * LEFT, 2 * RIGHT), Arrow(2 * DR, 2 * UL)]
        VGroup(*arrows).set_x(0).arrange(buff=2)
        self.play(GrowArrow(arrows[0]))
        self.play(GrowArrow(arrows[1], point_color=RED))

class GrowFromCenterExample(Scene):
    def construct(self):
        squares = [Square() for _ in range(2)]
        VGroup(*squares).set_x(0).arrange(buff=2)
        self.play(GrowFromCenter(squares[0]))
        self.play(GrowFromCenter(squares[1], point_color=RED))

class GrowFromEdgeExample(Scene):
    def construct(self):
        squares = [Square() for _ in range(4)]
        VGroup(*squares).set_x(0).arrange(buff=1)
        self.play(GrowFromEdge(squares[0], DOWN))
        self.play(GrowFromEdge(squares[1], RIGHT))
        self.play(GrowFromEdge(squares[2], UR))
        self.play(GrowFromEdge(squares[3], UP, point_color=RED))

class GrowFromPointExample(Scene):
    def construct(self):
        dot = Dot(3 * UR, color=GREEN)
        squares = [Square() for _ in range(4)]
        VGroup(*squares).set_x(0).arrange(buff=1)
        self.add(dot)
        self.play(GrowFromPoint(squares[0], ORIGIN))
        self.play(GrowFromPoint(squares[1], [-2, 2, 0]))
        self.play(GrowFromPoint(squares[2], [3, -2, 0], RED))
        self.play(GrowFromPoint(squares[3], dot, dot.get_color()))
        
class SpinInFromNothingExample(Scene):
    def construct(self):
        squares = [Square() for _ in range(3)]
        VGroup(*squares).set_x(0).arrange(buff=2)
        self.play(SpinInFromNothing(squares[0]))
        self.play(SpinInFromNothing(squares[1], angle=2 * PI))
        self.play(SpinInFromNothing(squares[2], point_color=RED))