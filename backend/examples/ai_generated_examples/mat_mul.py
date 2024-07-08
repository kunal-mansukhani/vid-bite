from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService

class MS(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            AzureService(
                voice="en-US-AriaNeural",
                style="newscast-casual",
            )
        )
        # Define the matrices
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[5, 6], [7, 8]])

        # Display the matrices
        vG = VGroup(m1, m2).arrange(RIGHT, buff=2)
        self.play(Create(vG))

        with self.voiceover(text="Let's multiply these two matrices together.") as tracker:
            self.wait(tracker.duration)
        
        # Highlight the first row of m1
        self.play(m1.get_rows()[0].animate.set_color(YELLOW))

        with self.voiceover(text="We take the dot product of the first row of the first matrix, ") as tracker:
            self.wait(tracker.duration)

        # Highlight the first column of m2
        self.play(m2.get_columns()[0].animate.set_color(YELLOW))

        with self.voiceover(text="and the first column of the second matrix.") as tracker:
            self.wait(tracker.duration)

        # Calculate the first entry
        e1 = (1 * 5) + (2 * 7)

        # Display the calculation
        calc = MathTex(f"(1)*(5) + (2)*(7) = {e1}")\
            .shift(DOWN*2).scale(0.75)
        self.play(Write(calc))

        with self.voiceover(text=f"This gives us {e1}, the first entry of the resulting matrix.") as tracker:
            self.wait(tracker.duration)

        # Create the resulting matrix
        m3 = Matrix([[e1, 0], [0, 0]]).move_to(RIGHT*2)
        self.play(Create(m3))

        with self.voiceover(text="We place this value in the first row and first column of the resulting matrix.") as tracker:
            self.wait(tracker.duration)

        # Reset colors
        self.play(m1.get_rows()[0].animate.set_color(WHITE), m2.get_columns()[0].animate.set_color(WHITE))
        self.play(FadeOut(calc))

        # Calculate the remaining entries
        for i in range(2):
            for j in range(2):
                if i == 0 and j == 0:
                    continue
                # Highlight the corresponding row and column
                self.play(m1.get_rows()[i].animate.set_color(YELLOW), m2.get_columns()[j].animate.set_color(YELLOW))

                # Calculate the entry
                entry = (int(m1.get_entries()[i*2].tex_string) * int(m2.get_entries()[j].tex_string)) + \
                        (int(m1.get_entries()[i*2+1].tex_string) * int(m2.get_entries()[j+2].tex_string))

                # Display the calculation
                calc = MathTex(f"({m1.get_entries()[i*2].tex_string})*({m2.get_entries()[j].tex_string}) + " +
                               f"({m1.get_entries()[i*2+1].tex_string})*({m2.get_entries()[j+2].tex_string}) = {entry}")\
                    .shift(DOWN*2).scale(0.75)
                self.play(Write(calc))

                with self.voiceover(text=f"For the entry in row {i+1} and column {j+1}, we get {entry}.") as tracker:
                    self.wait(tracker.duration)

                # Update the resulting matrix
                m3.get_entries()[i*2+j].become(MathTex(str(entry)))

                # Reset colors
                self.play(m1.get_rows()[i].animate.set_color(WHITE), m2.get_columns()[j].animate.set_color(WHITE))
                self.play(FadeOut(calc))

        # Final view
        self.wait(2)