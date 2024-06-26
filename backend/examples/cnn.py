from manim import *

class CNNAnimation(Scene):
    def create_grid(self, rows, cols, square_size=0.5, colors=None):
        grid = VGroup()
        for i in range(rows):
            for j in range(cols):
                square = Square(side_length=square_size)
                square.move_to([j * square_size, -i * square_size, 0])
                if colors:
                    square.set_fill(colors[i][j], opacity=0.8)
                grid.add(square)
        return grid

    def create_kernel(self, size=3, square_size=0.3):
        kernel = self.create_grid(size, size, square_size)
        kernel.set_stroke(WHITE, opacity=1)
        for i, square in enumerate(kernel):
            num = Text(str(i + 1), font_size=20)
            num.move_to(square.get_center())
            kernel.add(num)
        return kernel

    def slide_kernel(self, kernel, input_grid, output_grid):
        animations = []
        for i in range(4):
            for j in range(4):
                new_pos = input_grid[i * 6 + j].get_center()
                animations.append(kernel.animate.move_to(new_pos))
                output_square = output_grid[i * 4 + j]
                animations.append(output_square.animate.set_fill(YELLOW, opacity=0.8))
        return animations

    def construct(self):
        # Introduction
        title = Text("Convolutional Neural Networks (CNNs)")
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Input Image
        input_colors = [[BLUE, GREEN, RED, YELLOW, PURPLE, ORANGE] * 6 for _ in range(6)]
        input_grid = self.create_grid(6, 6, colors=input_colors)
        self.play(Create(input_grid))
        self.play(input_grid.animate.to_edge(LEFT))

        # Convolutional Layer
        kernel = self.create_kernel()
        kernel.next_to(input_grid, RIGHT)
        self.play(FadeIn(kernel))

        output_grid = self.create_grid(4, 4)
        output_grid.next_to(kernel, RIGHT)
        self.play(Create(output_grid))

        self.play(*self.slide_kernel(kernel, input_grid, output_grid))

        # Activation Function
        relu_text = Text("ReLU Activation", font_size=24)
        relu_text.next_to(output_grid, UP)
        self.play(Write(relu_text))
        self.play(*[square.animate.set_fill(RED_A if i % 2 == 0 else BLUE_A) for i, square in enumerate(output_grid)])
        self.play(FadeOut(relu_text))

        # Pooling Layer
        pooling_window = Square(side_length=0.5, stroke_color=YELLOW)
        pooling_window.move_to(output_grid[0].get_center())
        self.play(Create(pooling_window))

        pooled_grid = self.create_grid(2, 2, square_size=0.4)
        pooled_grid.next_to(output_grid, RIGHT)
        self.play(Create(pooled_grid))

        for i in range(2):
            for j in range(2):
                self.play(pooling_window.animate.move_to(output_grid[i * 8 + j * 2].get_center()))
                self.play(pooled_grid[i * 2 + j].animate.set_fill(YELLOW, opacity=0.8))

        self.play(FadeOut(pooling_window))

        # Fully Connected Layer
        fc_layer = VGroup(*[Dot() for _ in range(4)])
        fc_layer.arrange(DOWN)
        fc_layer.next_to(pooled_grid, RIGHT)
        self.play(Create(fc_layer))

        connections = VGroup()
        for i in range(4):
            for j in range(4):
                line = Line(pooled_grid[i].get_center(), fc_layer[j].get_center(), stroke_width=0.5)
                connections.add(line)
        self.play(Create(connections))

        self.play(*[dot.animate.set_color(YELLOW) for dot in fc_layer])

        # Conclusion
        self.play(
            Group(input_grid, kernel, output_grid, pooled_grid, fc_layer, connections).animate.scale(0.7).to_edge(LEFT)
        )

        final_title = Text("Convolutional Neural Networks", font_size=36)
        final_title.to_edge(UP)
        self.play(Write(final_title))

        explanation = Text("Input → Conv → ReLU → Pool → FC", font_size=24)
        explanation.next_to(final_title, DOWN)
        self.play(Write(explanation))

        self.wait(2)
