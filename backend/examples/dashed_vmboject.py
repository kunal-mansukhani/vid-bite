from manim import *

class DashedVMobjectExample(Scene):
    def construct(self):
        r = 0.5

        top_row = VGroup()  # Increasing num_dashes
        for dashes in range(1, 12):
            circ = DashedVMobject(Circle(radius=r, color=WHITE), num_dashes=dashes)
            top_row.add(circ)

        middle_row = VGroup()  # Increasing dashed_ratio
        for ratio in np.arange(1 / 11, 1, 1 / 11):
            circ = DashedVMobject(
                Circle(radius=r, color=WHITE), dashed_ratio=ratio
            )
            middle_row.add(circ)

        func1 = FunctionGraph(lambda t: t**5,[-1,1],color=WHITE)
        func_even = DashedVMobject(func1,num_dashes=6,equal_lengths=True)
        func_stretched = DashedVMobject(func1, num_dashes=6, equal_lengths=False)
        bottom_row = VGroup(func_even,func_stretched)

        top_row.arrange(buff=0.3)
        middle_row.arrange()
        bottom_row.arrange(buff=1)
        everything = VGroup(top_row, middle_row, bottom_row).arrange(DOWN, buff=1)
        self.add(everything)