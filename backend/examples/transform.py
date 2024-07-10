from manim import *

class TransformPathArc(Scene):
    def construct(self):
        def make_arc_path(start, end, arc_angle):
            points = []
            p_fn = path_along_arc(arc_angle)
            # alpha animates between 0.0 and 1.0, where 0.0
            # is the beginning of the animation and 1.0 is the end.
            for alpha in range(0, 11):
                points.append(p_fn(start, end, alpha / 10.0))
            path = VMobject(stroke_color=YELLOW)
            path.set_points_smoothly(points)
            return path

        left = Circle(stroke_color=BLUE_E, fill_opacity=1.0, radius=0.5).move_to(LEFT * 2)
        colors = [TEAL_A, TEAL_B, TEAL_C, TEAL_D, TEAL_E, GREEN_A]
        # Positive angles move counter-clockwise, negative angles move clockwise.
        examples = [-90, 0, 30, 90, 180, 270]
        anims = []
        for idx, angle in enumerate(examples):
            left_c = left.copy().shift((3 - idx) * UP)
            left_c.fill_color = colors[idx]
            right_c = left_c.copy().shift(4 * RIGHT)
            path_arc = make_arc_path(left_c.get_center(), right_c.get_center(),
                                     arc_angle=angle * DEGREES)
            desc = Text('%d°' % examples[idx]).next_to(left_c, LEFT)
            # Make the circles in front of the text in front of the arcs.
            self.add(
                path_arc.set_z_index(1),
                desc.set_z_index(2),
                left_c.set_z_index(3),
            )
            anims.append(Transform(left_c, right_c, path_arc=angle * DEGREES))

        self.play(*anims, run_time=2)
        self.wait()