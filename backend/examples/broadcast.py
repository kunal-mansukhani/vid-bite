from manim import *

class BroadcastExample(Scene):
    def construct(self):
        mob = Circle(radius=4, color=TEAL_A)
        self.play(Broadcast(mob))