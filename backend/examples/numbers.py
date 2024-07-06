from manim import *

class MovingSquareWithUpdaters(Scene):
    def construct(self):
        decimal = DecimalNumber(
            0,
            show_ellipsis=True,
            num_decimal_places=3,
            include_sign=True,
            unit=r"     ext{M-Units}",
            unit_buff_per_font_unit=0.003
        )
        square = Square().to_edge(UP)

        decimal.add_updater(lambda d: d.next_to(square, RIGHT))
        decimal.add_updater(lambda d: d.set_value(square.get_center()[1]))
        self.add(square, decimal)
        self.play(
            square.animate.to_edge(DOWN),
            rate_func=there_and_back,
            run_time=5,
        )
        self.wait()

class IntegerExample(Scene):
    def construct(self):
        self.add(Integer(number=2.5).set_color(ORANGE).scale(2.5).set_x(-0.5).set_y(0.8))
        self.add(Integer(number=3.14159, show_ellipsis=True).set_x(3).set_y(3.3).scale(3.14159))
        self.add(Integer(number=42).set_x(2.5).set_y(-2.3).set_color_by_gradient(BLUE, TEAL).scale(1.7))
        self.add(Integer(number=6.28).set_x(-1.5).set_y(-2).set_color(YELLOW).scale(1.4))

class VariablesWithValueTracker(Scene):
    def construct(self):
        var = 0.5
        on_screen_var = Variable(var, Text("var"), num_decimal_places=3)

        # You can also change the colours for the label and value
        on_screen_var.label.set_color(RED)
        on_screen_var.value.set_color(GREEN)

        self.play(Write(on_screen_var))
        # The above line will just display the variable with
        # its initial value on the screen. If you also wish to
        # update it, you can do so by accessing the `tracker` attribute
        self.wait()
        var_tracker = on_screen_var.tracker
        var = 10.5
        self.play(var_tracker.animate.set_value(var))
        self.wait()

        int_var = 0
        on_screen_int_var = Variable(
            int_var, Text("int_var"), var_type=Integer
        ).next_to(on_screen_var, DOWN)
        on_screen_int_var.label.set_color(RED)
        on_screen_int_var.value.set_color(GREEN)

        self.play(Write(on_screen_int_var))
        self.wait()
        var_tracker = on_screen_int_var.tracker
        var = 10.5
        self.play(var_tracker.animate.set_value(var))
        self.wait()

        # If you wish to have a somewhat more complicated label for your
        # variable with subscripts, superscripts, etc. the default class
        # for the label is MathTex
        subscript_label_var = 10
        on_screen_subscript_var = Variable(subscript_label_var, "{a}_{i}").next_to(
            on_screen_int_var, DOWN
        )
        self.play(Write(on_screen_subscript_var))
        self.wait()
class VariableExample(Scene):
    def construct(self):
        start = 2.0

        x_var = Variable(start, 'x', num_decimal_places=3)
        sqr_var = Variable(start**2, 'x^2', num_decimal_places=3)
        Group(x_var, sqr_var).arrange(DOWN)

        sqr_var.add_updater(lambda v: v.tracker.set_value(x_var.tracker.get_value()**2))

        self.add(x_var, sqr_var)
        self.play(x_var.tracker.animate.set_value(5), run_time=2, rate_func=linear)
        self.wait(0.1)
