from manim import *

class ArcShapeIris(Scene):
    def construct(self):
        colors = [DARK_BROWN, BLUE_E, BLUE_D, BLUE_A, TEAL_B, GREEN_B, YELLOW_E]
        radius = [1 + rad * 0.1 for rad in range(len(colors))]

        circles_group = VGroup()

        # zip(radius, color) makes the iterator [(radius[i], color[i]) for i in range(radius)]
        circles_group.add(*[Circle(radius=rad, stroke_width=10, color=col)
                            for rad, col in zip(radius, colors)])
        self.add(circles_group)

class AddToVGroup(Scene):
    def construct(self):
        circle_red = Circle(color=RED)
        circle_green = Circle(color=GREEN)
        circle_blue = Circle(color=BLUE)
        circle_red.shift(LEFT)
        circle_blue.shift(RIGHT)
        gr = VGroup(circle_red, circle_green)
        gr2 = VGroup(circle_blue) # Constructor uses add directly
        self.add(gr,gr2)
        self.wait()
        gr += gr2 # Add group to another
        self.play(
            gr.animate.shift(DOWN),
        )
        gr -= gr2 # Remove group
        self.play( # Animate groups separately
            gr.animate.shift(LEFT),
            gr2.animate.shift(UP),
        )
        self.play( #Animate groups without modification
            (gr+gr2).animate.shift(RIGHT)
        )
        self.play( # Animate group without component
            (gr-circle_red).animate.shift(RIGHT)
        )
