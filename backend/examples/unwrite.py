from manim import *

class UnwriteReverseTrue(Scene):
    def construct(self):
        text = Tex("Alice and Bob").scale(3)
        self.add(text)
        self.play(Unwrite(text))