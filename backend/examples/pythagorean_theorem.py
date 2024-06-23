from manim import *

class AnGen(Scene):
    def construct(self):
        # Scene 1: Repeated Addition
        circles1 = VGroup(*[Circle(color=RED) for _ in range(2)])
        circles2 = circles1.copy()
        circles3 = circles1.copy()

        circles1.arrange(RIGHT, buff=0.5)
        circles2.arrange(RIGHT, buff=0.5).next_to(circles1, RIGHT, buff=1)
        circles3.arrange(RIGHT, buff=0.5).next_to(circles2, RIGHT, buff=1)

        addition_text = Text("2 + 2 + 2").next_to(circles2, DOWN)
        self.play(Create(circles1), Create(circles2), Create(circles3), Write(addition_text))
        self.wait(1)

        self.play(circles1.animate.shift(LEFT * 2), circles3.animate.shift(RIGHT * 2))
        self.wait(1)

        all_circles = VGroup(circles1, circles2, circles3)
        combined_circles = all_circles.copy().arrange(RIGHT, buff=0.5)
        equals_text = Text("=").next_to(addition_text, RIGHT)
        six_text = Text("6").next_to(equals_text, RIGHT)
        self.play(Transform(all_circles, combined_circles), Write(equals_text), Write(six_text))
        self.wait(2)

        # Scene 2: Introducing Multiplication
        self.play(FadeOut(all_circles), FadeOut(addition_text), FadeOut(equals_text), FadeOut(six_text))

        multiplication_text = Text("3 x 2 = 6")
        multiplication_text.set_color_by_tex("x", YELLOW)
        self.play(Write(multiplication_text))

        explanation_text = Text("3 groups of 2").next_to(multiplication_text, DOWN)
        self.play(Write(explanation_text))

        arrow1 = Arrow(multiplication_text[0].get_bottom(), combined_circles.get_top())
        arrow2 = Arrow(multiplication_text[2].get_bottom(), circles1.get_top())
        self.play(Create(arrow1), Create(arrow2))
        self.wait(2)

        # Scene 3: Array Representation
        self.play(FadeOut(multiplication_text), FadeOut(explanation_text), FadeOut(arrow1), FadeOut(arrow2), FadeOut(combined_circles))

        dot_array = VGroup(*[Dot(color=RED) for _ in range(6)]).arrange_in_grid(3, 2)
        array_text = Text("3 x 2 = 6").next_to(dot_array, DOWN)
        self.play(Create(dot_array), Write(array_text))
        self.wait(1)

        for row in range(3):
            self.play(dot_array[row * 2:row * 2 + 2].animate.set_color(BLUE), run_time=0.5)
            self.wait(0.5)
            self.play(dot_array[row * 2:row * 2 + 2].animate.set_color(RED), run_time=0.5)

        # Scene 4: Commutative Property
        self.wait(1)

        dot_array2 = VGroup(*[Dot(color=RED) for _ in range(6)]).arrange_in_grid(2, 3)
        dot_array2.next_to(dot_array, RIGHT, buff=2)
        array_text2 = Text("2 x 3 = 6").next_to(dot_array2, DOWN)
        self.play(TransformFromCopy(dot_array, dot_array2), Write(array_text2))
        self.wait(1)

        for i in range(3):
            self.play(dot_array[i * 2:i * 2 + 2].animate.set_color(BLUE),
                      dot_array2[i::3].animate.set_color(BLUE), run_time=0.5)
            self.wait(0.5)
            self.play(dot_array[i * 2:i * 2 + 2].animate.set_color(RED),
                      dot_array2[i::3].animate.set_color(RED), run_time=0.5)

        self.wait(2)


if __name__ == "__main__":
    scene = AnGen()
    scene.render()

