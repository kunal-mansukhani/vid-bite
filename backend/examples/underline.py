from manim import *

class UnderLine(Scene):
    def construct(self):
        man = Tex("Manim")  # Full Word
        ul = Underline(man)  # Underlining the word
        self.add(man, ul)