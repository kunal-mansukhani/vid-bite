from manim import *

class FadeInExample(Scene):
    def construct(self):
        dot = Dot(UP * 2 + LEFT)
        self.add(dot)
        tex = Tex(
            "FadeIn with ", "shift ", " or target\_position", " and scale"
        ).scale(1)
        animations = [
            FadeIn(tex[0]),
            FadeIn(tex[1], shift=DOWN),
            FadeIn(tex[2], target_position=dot),
            FadeIn(tex[3], scale=1.5),
        ]
        self.play(AnimationGroup(*animations, lag_ratio=0.5))
        
class FadeInExample(Scene):
    def construct(self):
        dot = Dot(UP * 2 + LEFT)
        self.add(dot)
        tex = Tex(
            "FadeOut with ", "shift ", " or target\_position", " and scale"
        ).scale(1)
        animations = [
            FadeOut(tex[0]),
            FadeOut(tex[1], shift=DOWN),
            FadeOut(tex[2], target_position=dot),
            FadeOut(tex[3], scale=0.5),
        ]
        self.play(AnimationGroup(*animations, lag_ratio=0.5))