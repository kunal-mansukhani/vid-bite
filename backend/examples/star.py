from manim import *

class StarExample(Scene):
    def construct(self):
        pentagram = RegularPolygram(5, radius=2)
        star = Star(outer_radius=2, color=RED)

        self.add(pentagram)
        self.play(Create(star), run_time=3)
        self.play(FadeOut(star), run_time=2)
class DifferentDensitiesExample(Scene):
    def construct(self):
        density_2 = Star(7, outer_radius=2, density=2, color=RED)
        density_3 = Star(7, outer_radius=2, density=3, color=PURPLE)

        self.add(VGroup(density_2, density_3).arrange(RIGHT))