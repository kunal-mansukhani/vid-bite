from manim import *

class TransformerAnimation(Scene):
    def create_token_squares(self, colors):
        return VGroup(*[Square(side_length=0.5, fill_opacity=0.8, color=color) for color in colors])

    def create_embeddings(self, squares):
        return VGroup(*[Rectangle(height=2, width=0.3, fill_opacity=0.8, color=square.get_color()) for square in squares])

    def create_attention_head(self, embeddings, color):
        head = VGroup()
        for i, emb1 in enumerate(embeddings):
            for j, emb2 in enumerate(embeddings):
                line = Line(emb1.get_bottom(), emb2.get_top(), stroke_width=1, color=color)
                line.set_opacity((i + j) % 5 * 0.2)  # Vary opacity for visualization
                head.add(line)
        return head

    def construct(self):
        # 1. Introduction
        title = Text("Understanding Transformers", font_size=48)
        self.play(Write(title))
        self.play(title.animate.scale(0.5).to_edge(UP))
        self.wait(1)

        # 2. Input Sequence
        colors = [BLUE, RED, GREEN, YELLOW, PURPLE]
        input_seq = self.create_token_squares(colors)
        input_seq.arrange(RIGHT, buff=0.2)
        input_label = Text("Input Sequence", font_size=24).next_to(input_seq, DOWN)
        self.play(Create(input_seq), Write(input_label))
        self.play(input_seq.animate.to_edge(LEFT), input_label.animate.to_edge(LEFT, buff=1))

        # 3. Embedding Layer
        embeddings = self.create_embeddings(input_seq)
        embeddings.arrange(RIGHT, buff=0.5).next_to(input_seq, UP, buff=1)
        embedding_label = Text("Embedding Layer", font_size=24).next_to(embeddings, DOWN)
        
        self.play(
            *[Transform(square.copy(), embedding) for square, embedding in zip(input_seq, embeddings)],
            Write(embedding_label)
        )
        self.wait(1)

        # 4. Positional Encoding
        pos_encodings = VGroup(*[
            FunctionGraph(
                lambda x: 0.5 * np.sin(x * 5 + i),
                x_range=[-1, 1, 0.01],
                color=YELLOW
            ).move_to(embedding).match_height(embedding).set_stroke(width=2)
            for i, embedding in enumerate(embeddings)
        ])
        pos_encoding_label = Text("Positional Encoding", font_size=24).next_to(pos_encodings, DOWN)
        
        self.play(Create(pos_encodings), Write(pos_encoding_label))
        self.play(
            *[embedding.animate.set_opacity(0.5) for embedding in embeddings],
            *[encoding.animate.set_opacity(0.5) for encoding in pos_encodings]
        )
        encoded_embeddings = embeddings.copy().set_opacity(1)
        self.play(
            FadeOut(pos_encodings),
            FadeOut(pos_encoding_label),
            FadeOut(embedding_label),
            encoded_embeddings.animate.shift(UP * 2)
        )

        # 5. Multi-Head Attention
        attention_heads = VGroup(*[
            self.create_attention_head(encoded_embeddings, color)
            for color in [BLUE, RED, GREEN]
        ])
        attention_label = Text("Multi-Head Attention", font_size=24).next_to(attention_heads, DOWN)
        
        self.play(Create(attention_heads[0]))
        self.play(
            Create(attention_heads[1]),
            Create(attention_heads[2])
        )
        self.play(Write(attention_label))
        self.wait(1)

        # 6. Add & Norm
        add_norm_box = Rectangle(height=4, width=6, stroke_color=WHITE)
        add_norm_label = Text("Add & Norm", font_size=24).next_to(add_norm_box, DOWN)
        add_norm_group = VGroup(add_norm_box, add_norm_label).next_to(encoded_embeddings, DOWN, buff=1)
        
        self.play(
            FadeOut(attention_heads),
            FadeOut(attention_label),
            Create(add_norm_box),
            Write(add_norm_label)
        )
        self.play(add_norm_group.animate.shift(RIGHT * 3))

        # 7. Feed-Forward Network
        ffn_box = Rectangle(height=3, width=2, stroke_color=WHITE)
        ffn_label = Text("Feed-Forward\nNetwork", font_size=24).next_to(ffn_box, DOWN)
        ffn_group = VGroup(ffn_box, ffn_label).next_to(add_norm_group, RIGHT)
        
        self.play(Create(ffn_box), Write(ffn_label))
        self.wait(1)

        # 8. Output Sequence
        output_seq = self.create_token_squares(colors)
        output_seq.arrange(RIGHT, buff=0.2).next_to(ffn_group, RIGHT)
        output_label = Text("Output Sequence", font_size=24).next_to(output_seq, DOWN)
        
        self.play(
            ReplacementTransform(encoded_embeddings, output_seq),
            Write(output_label)
        )
        self.wait(1)

        # 9. Full Architecture
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != title],
            title.animate.scale(1.5).move_to(ORIGIN)
        )
        
        encoder = Rectangle(height=5, width=3, stroke_color=BLUE).shift(LEFT * 3)
        encoder_label = Text("Encoder", color=BLUE).next_to(encoder, DOWN)
        decoder = Rectangle(height=5, width=3, stroke_color=RED).shift(RIGHT * 3)
        decoder_label = Text("Decoder", color=RED).next_to(decoder, DOWN)
        
        self.play(
            Create(encoder),
            Create(decoder),
            Write(encoder_label),
            Write(decoder_label)
        )

        # 10. Conclusion
        key_points = VGroup(
            Text("• Self-Attention", font_size=24),
            Text("• Parallelization", font_size=24),
            Text("• Long-range dependencies", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(decoder, RIGHT)
        
        final_title = Text("Transformers: Attention Is All You Need", color=YELLOW).to_edge(DOWN)
        
        self.play(Write(key_points), run_time=2)
        self.play(Write(final_title))
        
        self.wait(2)