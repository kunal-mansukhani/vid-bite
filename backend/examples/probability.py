from manim import *

class BarChartExample(Scene):
    def construct(self):
        chart = BarChart(
            values=[-5, 40, -10, 20, -3],
            bar_names=["one", "two", "three", "four", "five"],
            y_range=[-20, 50, 10],
            y_length=6,
            x_length=10,
            x_axis_config={"font_size": 36},
        )

        c_bar_lbls = chart.get_bar_labels(font_size=48)

        self.add(chart, c_bar_lbls)

class ExampleSampleSpace(Scene):
    def construct(self):
        poly1 = SampleSpace(stroke_width=15, fill_opacity=1)
        poly2 = SampleSpace(width=5, height=3, stroke_width=5, fill_opacity=0.5)
        poly3 = SampleSpace(width=2, height=2, stroke_width=5, fill_opacity=0.1)
        poly3.divide_vertically(p_list=np.array([0.37, 0.13, 0.5]), colors=[BLACK, WHITE, GRAY], vect=RIGHT)
        poly_group = VGroup(poly1, poly2, poly3).arrange()
        self.add(poly_group)
