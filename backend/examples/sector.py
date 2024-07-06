from manim import *

class ExampleSector(Scene):
    def construct(self):
        sector = Sector(outer_radius=2, inner_radius=1)
        sector2 = Sector(outer_radius=2.5, inner_radius=0.8).move_to([-3, 0, 0])
        sector.set_color(RED)
        sector2.set_color(PINK)
        self.add(sector, sector2)