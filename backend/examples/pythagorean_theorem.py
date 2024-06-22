from manim import *

class PythagoreanTheorem(Scene):
    def construct(self):
        # Create the right triangle
        triangle = Polygon(ORIGIN, 4 * RIGHT, 3 * UP, color=WHITE)
        
        # Label the sides
        labels = VGroup(
            MathTex("a").next_to(triangle.get_bottom(), DOWN),
            MathTex("b").next_to(triangle.get_right(), RIGHT),
            MathTex("c").next_to(triangle.get_center(), UL)
        )
        
        # Create squares on each side
        square_a = Square(side_length=3, fill_opacity=0.5, color=RED).align_to(triangle, LEFT).shift(UP * 3)
        square_b = Square(side_length=4, fill_opacity=0.5, color=GREEN).align_to(triangle, DOWN).shift(RIGHT * 4)
        square_c = Square(side_length=5, fill_opacity=0.5, color=BLUE).rotate(np.arctan(3/4)).move_to(triangle.get_center())
        
        # Create labels for areas
        area_labels = VGroup(
            MathTex("a^2").move_to(square_a.get_center()),
            MathTex("b^2").move_to(square_b.get_center()),
            MathTex("c^2").move_to(square_c.get_center())
        )
        
        # Create the equation
        equation = MathTex("a^2", "+", "b^2", "=", "c^2").to_edge(DOWN)
        
        # Animations
        self.play(Create(triangle))
        self.play(Write(labels))
        self.wait()
        
        self.play(
            Create(square_c),
            FadeIn(square_c, shift=DOWN),
            run_time=1.5
        )
        self.play(Write(area_labels[2]))
        self.wait()
        
        self.play(
            Create(square_a),
            Create(square_b),
            FadeIn(square_a, shift=RIGHT),
            FadeIn(square_b, shift=UP),
            run_time=1.5
        )
        self.play(Write(area_labels[0]), Write(area_labels[1]))
        self.wait()
        
        self.play(Write(equation))
        
        # Highlight the equality
        self.play(
            square_c.animate.set_fill(opacity=0.8),
            square_a.animate.set_fill(opacity=0.8),
            square_b.animate.set_fill(opacity=0.8)
        )
        self.wait()
        
        # Show the squares moving
        self.play(
            square_a.animate.shift(DOWN * 3),
            square_b.animate.shift(LEFT * 4),
            run_time=2
        )
        self.wait()
        
        # Final emphasis
        self.play(
            Indicate(square_a, scale_factor=1.05),
            Indicate(square_b, scale_factor=1.05),
            Indicate(square_c, scale_factor=1.05),
            Indicate(equation, scale_factor=1.1),
            run_time=2
        )
        self.wait(2)

if __name__ == "__main__":
    config.background_color = WHITE
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_width = 16
    config.frame_height = 9
    scene = PythagoreanTheorem()
    scene.render()

