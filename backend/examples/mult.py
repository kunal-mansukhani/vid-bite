from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService

class MultiplicationVisualization(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            AzureService(
                voice="en-US-AriaNeural",
                style="newscast-casual",
            )
        )
        
        # Scene 1: Introduction
        t1 = Text("Multiplication").to_edge(UP)
        s1 = Square(color=BLUE).scale(0.5)
        label1 = Text("1").move_to(s1.get_center())  # Create a separate Text object for the label
        c1 = Circle(color=GREEN).scale(0.5)
        label3 = Text("3").move_to(c1.get_center())  # Create a separate Text object for the label
        c1.next_to(s1, RIGHT)
        
        with self.voiceover(text="Multiplication is a way of combining numbers. Let's see how it works!") as t:
            self.play(FadeIn(s1), FadeIn(label1), FadeIn(c1), FadeIn(label3), FadeIn(t1))
            self.wait(t.duration)

        self.play(FadeOut(t1))
        self.camera.frame.set(width=self.camera.frame.get_width() * 1.2).move_to(s1)
        
        # Scene 2: Repeated Addition
        s2 = s1.copy()
        s3 = s1.copy()
        sr = VGroup(s1, s2, s3).arrange(RIGHT, buff=0.5)
        d1 = DashedLine(c1.get_right(), s3.get_left())
        t2 = MathTex("3", "\\times", "1").next_to(sr, DOWN)
        t2[1].scale(1.2).set_color(YELLOW)

        with self.voiceover(text="Three times one is like adding one three times.") as t:
            self.play(FadeIn(s2, shift=RIGHT), FadeIn(s3, shift=RIGHT), FadeIn(d1), FadeIn(t2))
            self.wait(t.duration)

        self.camera.frame.set(width=self.camera.frame.get_width() * 1.2).move_to(sr)
        
        # Scene 3: Result
        s4 = Square(color=BLUE).scale(1.2)
        label3 = Text("3").move_to(s4.get_center())  # Create a separate Text object for the label
        s4.next_to(sr, DOWN)
        t3 = MathTex("3", "\\times", "1", "=", "3").next_to(s4, DOWN)
        t3[1].scale(1.2).set_color(YELLOW)
        t3[3].scale(1.2).set_color(YELLOW)

        with self.voiceover(text="So, 3 times 1 equals 3!") as t:
            self.play(Transform(sr, s4), FadeOut(d1), FadeOut(t2), FadeIn(t3), FadeIn(label3))
            self.wait(t.duration)