from manim import *

class SpeedModifierExample(Scene):
    def construct(self):
        a = Dot().shift(LEFT * 4)
        b = Dot().shift(RIGHT * 4)
        self.add(a, b)
        self.play(
            ChangeSpeed(
                AnimationGroup(
                    a.animate(run_time=1).shift(RIGHT * 8),
                    b.animate(run_time=1).shift(LEFT * 8),
                ),
                speedinfo={0.3: 1, 0.4: 0.1, 0.6: 0.1, 1: 1},
                rate_func=linear,
            )
        )