from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService

class PD(VoiceoverScene, ThreeDScene):
    def construct(self):
        # Set up Azure voice service
        self.set_speech_service(
            AzureService(
                voice="en-US-AriaNeural",
                style="newscast-casual",
            )
        )
        
        # Create the 3D axes
        ax = ThreeDAxes(
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
            z_range=(-2, 2, 1),
            axis_config={"include_tip": False, "include_numbers": True, "font_size": 24},
        ).scale(0.7)
        
        # Define the function z = f(x, y) = x^2 - y^2
        def f(x, y):
            return x**2 - y**2
        
        # Create the surface
        sf = Surface(
            lambda u, v: ax.c2p(u, v, f(u, v)),
            u_range=(-2, 2),
            v_range=(-2, 2),
            resolution=(30, 30),
            should_make_jagged=True,
        )
        sf.set_style(fill_opacity=0.7, stroke_color=BLUE, stroke_width=0.5)
        
        # Create labels for axes
        x_l = MathTex("x").next_to(ax.x_axis, RIGHT)
        y_l = MathTex("y").next_to(ax.y_axis, UP)
        z_l = MathTex("z").next_to(ax.z_axis, OUT)
        lb = VGroup(x_l, y_l, z_l)
        
        # Create the scene
        sc = VGroup(ax, sf, lb)
        sc.scale(0.8).move_to(ORIGIN)
        
        # Animation
        with self.voiceover(text="Let's explore partial derivatives using a 3D surface."):
            self.set_camera_orientation(phi=75*DEGREES, theta=-30*DEGREES)
            self.play(Create(ax), run_time=2)
            self.play(FadeIn(sf), run_time=2)
            self.play(Write(lb), run_time=1)
        
        # Equation
        eq = MathTex("z", "=", "f(x,y)", "=", "x^2 - y^2")
        eq.to_corner(UL).scale(0.8)
        
        with self.voiceover(text="We'll use the function z equals x squared minus y squared."):
            self.play(Write(eq), run_time=2)
        
        # Partial derivative with respect to x
        with self.voiceover(text="The partial derivative with respect to x is found by treating y as a constant."):
            self.move_camera(phi=80*DEGREES, theta=-10*DEGREES, run_time=2)
            l1 = Line(ax.c2p(-2, 1, f(-2, 1)), ax.c2p(2, 1, f(2, 1)), color=RED)
            self.play(Create(l1), run_time=2)
        
        pd_x = MathTex(r"\frac{\partial z}{\partial x}", "=", "2x")
        pd_x.next_to(eq, DOWN, aligned_edge=LEFT).scale(0.8)
        
        with self.voiceover(text="This gives us the partial derivative: partial z over partial x equals 2x."):
            self.play(Write(pd_x), run_time=2)
        
        # Partial derivative with respect to y
        with self.voiceover(text="Similarly, for the partial derivative with respect to y, we treat x as a constant."):
            self.move_camera(phi=80*DEGREES, theta=-100*DEGREES, run_time=2)
            l2 = Line(ax.c2p(1, -2, f(1, -2)), ax.c2p(1, 2, f(1, 2)), color=GREEN)
            self.play(Create(l2), run_time=2)
        
        pd_y = MathTex(r"\frac{\partial z}{\partial y}", "=", "-2y")
        pd_y.next_to(pd_x, DOWN, aligned_edge=LEFT).scale(0.8)
        
        with self.voiceover(text="This gives us: partial z over partial y equals negative 2y."):
            self.play(Write(pd_y), run_time=2)
        
        # Conclusion
        with self.voiceover(text="Partial derivatives allow us to analyze how a function changes with respect to one variable while holding the others constant."):
            self.move_camera(phi=70*DEGREES, theta=-45*DEGREES, run_time=2)
            self.play(Indicate(VGroup(pd_x, pd_y)), run_time=2)
        
        self.wait(2)