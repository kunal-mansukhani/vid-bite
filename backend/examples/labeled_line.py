from manim import *

class LabeledLineExample(Scene):
    def construct(self):
        line = LabeledLine(
            label          = '0.5',
            label_position = 0.8,
            font_size      = 20,
            label_color    = WHITE,
            label_frame    = True,

            start=LEFT+DOWN,
            end=RIGHT+UP)

        line.set_length(line.get_length() * 2)
        self.add(line)

    class LabeledArrowExample(Scene):
        def construct(self):
            l_arrow = LabeledArrow("0.5", start=LEFT*3, end=RIGHT*3 + UP*2, label_position=0.5)

            self.add(l_arrow)