from manim import *

class ClockwiseExample(Scene):
    def construct(self):
        dl, dr = Dot(), Dot()
        sl, sr = Square(), Square()

        VGroup(dl, sl).arrange(DOWN).shift(2*LEFT)
        VGroup(dr, sr).arrange(DOWN).shift(2*RIGHT)

        self.add(dl, dr)
        self.wait()
        self.play(
            ClockwiseTransform(dl, sl),
            Transform(dr, sr)
        )
        self.wait()

class CounterclockwiseTransform_vs_Transform(Scene):
    def construct(self):
        # set up the numbers
        c_transform = VGroup(DecimalNumber(number=3.141, num_decimal_places=3), DecimalNumber(number=1.618, num_decimal_places=3))
        text_1 = Text("CounterclockwiseTransform", color=RED)
        c_transform.add(text_1)

        transform = VGroup(DecimalNumber(number=1.618, num_decimal_places=3), DecimalNumber(number=3.141, num_decimal_places=3))
        text_2 = Text("Transform", color=BLUE)
        transform.add(text_2)

        ints = VGroup(c_transform, transform)
        texts = VGroup(text_1, text_2).scale(0.75)
        c_transform.arrange(direction=UP, buff=1)
        transform.arrange(direction=UP, buff=1)

        ints.arrange(buff=2)
        self.add(ints, texts)

        # The mobs move in clockwise direction for ClockwiseTransform()
        self.play(CounterclockwiseTransform(c_transform[0], c_transform[1]))

        # The mobs move straight up for Transform()
        self.play(Transform(transform[0], transform[1]))