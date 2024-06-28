from manim import *

LIGHT_BLUE = "#89CFF0"

class BackpropagationAnimation(Scene):
    def construct(self):
        self.scene1_introduction()
        self.scene2_forward_pass_and_loss()
        self.scene3_backpropagation_begins()
        self.scene4_updating_weights()
        self.scene5_conclusion()

    def create_neural_network(self):
        layers = [2, 3, 1]
        network = VGroup()
        x_positions = [-3, 0, 3]
        
        for i, layer_size in enumerate(layers):
            layer = VGroup(*[Circle(radius=0.5, fill_opacity=0.8, color=BLUE_E) 
                             for _ in range(layer_size)])
            layer.arrange(DOWN, buff=1)
            layer.move_to(x_positions[i] * RIGHT)
            network.add(layer)

        for i in range(len(layers) - 1):
            for start_node in network[i]:
                for end_node in network[i+1]:
                    line = Line(start_node.get_center(), end_node.get_center(), 
                                stroke_width=3, color=LIGHT_GRAY)
                    network.add(line)

        return network

    def scene1_introduction(self):
        title = Text("Backpropagation", font_size=48, color=LIGHT_BLUE, weight=BOLD)
        self.play(FadeIn(title), run_time=2)
        self.wait(0.5)
        network = self.create_neural_network()
        self.play(FadeOut(title), FadeIn(network, shift=UP), run_time=1.5)
        return network

    def scene2_forward_pass_and_loss(self):
        network = self.create_neural_network()
        data_point = Square(side_length=0.3, fill_color=LIGHT_BLUE, fill_opacity=1)
        data_point.move_to(network[0][0].get_center())

        path = VMobject()
        path.set_points_smoothly([
            network[0][0].get_center(),
            network[1][1].get_center(),
            network[2][0].get_center()
        ])

        def get_data_point_updater(alpha):
            return lambda m, alpha: m.move_to(path.point_from_proportion(alpha))

        prediction = DecimalNumber(0.6, color=RED, font_size=24)
        prediction.next_to(network[2][0], RIGHT)
        target = DecimalNumber(1.0, color=GREEN, font_size=24)
        target.next_to(prediction, RIGHT)

        loss_label = Text("Loss Function", font_size=16, color=YELLOW)
        loss_label.next_to(network[2][0], UP)

        self.add(network)
        self.play(FadeIn(data_point))
        self.play(UpdateFromAlphaFunc(data_point, get_data_point_updater(0)),
                  UpdateFromAlphaFunc(data_point, get_data_point_updater(0.5)),
                  UpdateFromAlphaFunc(data_point, get_data_point_updater(1)),
                  run_time=3)
        
        self.play(Write(prediction), Write(target))
        self.play(Write(loss_label))
        
        for _ in range(3):
            self.play(loss_label.animate.set_color(RED), run_time=0.3)
            self.play(loss_label.animate.set_color(YELLOW), run_time=0.3)

        self.play(FadeOut(loss_label), FadeOut(data_point))
        return network, prediction, target

    def scene3_backpropagation_begins(self):
        network, prediction, target = self.scene2_forward_pass_and_loss()
        
        arrows = VGroup()
        for i in reversed(range(len(network) - 1)):
            for start_node in network[i+1]:
                for end_node in network[i]:
                    arrow = Arrow(start_node.get_center(), end_node.get_center(), 
                                  buff=0.1, color=RED)
                    arrows.add(arrow)

        self.play(GrowFromCenter(arrows), run_time=2)
        self.play(arrows.animate.set_color(GRAY), run_time=1)
        return network, arrows, prediction, target

    def scene4_updating_weights(self):
        network, arrows, prediction, target = self.scene3_backpropagation_begins()
        
        def create_weight_label(pos):
            return DecimalNumber(1, num_decimal_places=2, font_size=16).move_to(pos)

        weights = VGroup(*[create_weight_label(arrow.get_center()) for arrow in arrows[:3]])
        
        self.play(FadeIn(weights))
        
        for weight in weights:
            self.play(weight.animate.set_value(weight.get_value() + 0.5), run_time=1)

        self.play(FadeOut(weights), FadeOut(arrows))
        return network, prediction, target

    def scene5_conclusion(self):
        network, prediction, target = self.scene4_updating_weights()
        
        data_point = Square(side_length=0.3, fill_color=LIGHT_BLUE, fill_opacity=1)
        data_point.move_to(network[0][0].get_center())

        path = VMobject()
        path.set_points_smoothly([
            network[0][0].get_center(),
            network[1][1].get_center(),
            network[2][0].get_center()
        ])

        def get_data_point_updater(alpha):
            return lambda m, alpha: m.move_to(path.point_from_proportion(alpha))

        repeat_text = Text("Repeat. Improve.", font_size=24, color=YELLOW)
        repeat_text.to_edge(DOWN)

        self.play(FadeIn(data_point))
        self.play(UpdateFromAlphaFunc(data_point, get_data_point_updater(0)),
                  UpdateFromAlphaFunc(data_point, get_data_point_updater(0.5)),
                  UpdateFromAlphaFunc(data_point, get_data_point_updater(1)),
                  prediction.animate.set_value(0.9),
                  run_time=2)
        
        self.play(Write(repeat_text))
        
        for value in [0.95, 0.98]:
            self.play(
                UpdateFromAlphaFunc(data_point, get_data_point_updater(0)),
                UpdateFromAlphaFunc(data_point, get_data_point_updater(0.5)),
                UpdateFromAlphaFunc(data_point, get_data_point_updater(1)),
                prediction.animate.set_value(value),
                run_time=1.5
            )

        self.play(FadeOut(network), FadeOut(data_point), FadeOut(prediction), 
                  FadeOut(target), FadeOut(repeat_text))

if __name__ == "__main__":
    scene = BackpropagationAnimation()
    scene.render()