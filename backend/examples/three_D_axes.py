from manim import *

class GetAxisLabelsExample(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=2*PI/5, theta=PI/5)
        axes = ThreeDAxes()
        labels = axes.get_axis_labels(
            Text("x-axis").scale(0.7), Text("y-axis").scale(0.45), Text("z-axis").scale(0.45)
        )
        self.add(axes, labels)
class GetYAxisLabelExample(ThreeDScene):
    def construct(self):
        ax = ThreeDAxes()
        lab = ax.get_y_axis_label(Tex("$y$-label"))
        self.set_camera_orientation(phi=2*PI/5, theta=PI/5)
        self.add(ax, lab)
class GetYAxisLabelExample(ThreeDScene):
    def construct(self):
        ax = ThreeDAxes()
        lab = ax.get_y_axis_label(Tex("$y$-label"))
        self.set_camera_orientation(phi=2*PI/5, theta=PI/5)
        self.add(ax, lab)
class GetZAxisLabelExample(ThreeDScene):
    def construct(self):
        ax = ThreeDAxes()
        lab = ax.get_z_axis_label(Tex("$z$-label"))
        self.set_camera_orientation(phi=2*PI/5, theta=PI/5)
        self.add(ax, lab)