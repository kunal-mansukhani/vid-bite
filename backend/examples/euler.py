from manim import *

class PythagoreanTheorem(Scene):
    def construct(self):
        # Create the right triangle
        triangle = Polygon(
            np.array([-2, 0, 0]),
            np.array([2, 0, 0]),
            np.array([2, 3, 0]),
            color=BLUE,
            fill_opacity=0.5
        )
        self.play(Create(triangle))

        # Label the sides of the triangle
        a_label = MathTex("a").next_to(triangle.get_vertices()[0], DOWN)
        b_label = MathTex("b").next_to(triangle.get_vertices()[2], RIGHT)
        c_label = MathTex("c").next_to(triangle.get_vertices()[1], UP + LEFT)
        self.play(Write(a_label), Write(b_label), Write(c_label))

        # Create squares on each side of the triangle
        square_a = Square(side_length=4, color=RED, fill_opacity=0.5).move_to(np.array([-2, -2, 0]))
        square_b = Square(side_length=6, color=GREEN, fill_opacity=0.5).move_to(np.array([2, 3, 0]))
        square_c = Square(side_length=np.sqrt(4**2 + 6**2), color=YELLOW, fill_opacity=0.5).move_to(np.array([0, 1.5, 0]))

        # Rotate and move the squares to fit the sides of the triangle
        square_a.rotate(np.arctan(3/4), about_point=np.array([-2, 0, 0]))
        square_b.rotate(np.arctan(3/4), about_point=np.array([2, 3, 0]))
        square_c.rotate(np.arctan(3/4), about_point=np.array([2, 0, 0]))

        self.play(Create(square_a), Create(square_b), Create(square_c))

        # Write the Pythagorean theorem equation
        equation = MathTex("a^2 + b^2 = c^2").next_to(triangle, UP)
        self.play(Write(equation))

        self.wait(2)