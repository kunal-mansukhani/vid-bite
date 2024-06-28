from manim import *

class MatrixMultiplication(Scene):
    def construct(self):
        self.intro_scene()
        self.highlight_first_element()
        self.calculate_first_element()
        self.repeat_for_other_elements()
        self.final_result()
    
    def intro_scene(self):
        title = Text("Matrix Multiplication")
        self.play(FadeIn(title))
        self.wait(1)
        
        A = MathTex(r"A = \begin{pmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{pmatrix}")
        B = MathTex(r"B = \begin{pmatrix} b_{11} & b_{12} \\ b_{21} & b_{22} \end{pmatrix}")
        C = MathTex(r"C = \begin{pmatrix} c_{11} & c_{12} \\ c_{21} & c_{22} \end{pmatrix}")
        
        A.next_to(title, DOWN, buff=1)
        B.next_to(A, RIGHT, buff=1)
        C.next_to(A, DOWN, buff=1)
        
        self.play(FadeIn(A), FadeIn(B))
        self.play(FadeIn(C))
        self.wait(1)
        
        self.play(FadeOut(title), FadeOut(A), FadeOut(B))
        self.A = A
        self.B = B
        self.C = C
    
    def highlight_first_element(self):
        A, B, C = self.A, self.B, self.C
        highlight_B_row = SurroundingRectangle(B[0][5:7], color=GREEN, fill_opacity=0.3)
        arrow = Arrow(B[0][5:7].get_bottom(), C[0][1].get_top(), buff=0.1)
        step1_text = Text("Step 1: Multiply first row of B by the first column of A.").scale(0.5).to_edge(UP)
        eq1 = MathTex(r"b_{11} \cdot a_{11} + b_{12} \cdot a_{21}").next_to(C[0][0], RIGHT)
        
        self.play(FadeIn(highlight_B_row))
        self.play(Create(arrow), FadeIn(step1_text), FadeIn(eq1))
        self.wait(2)
        
        self.play(FadeOut(highlight_B_row), FadeOut(arrow))
        self.step1_text = step1_text
        self.eq1 = eq1
    
    def calculate_first_element(self):
        A, C, step1_text, eq1 = self.A, self.C, self.step1_text, self.eq1
        highlight_A_col = SurroundingRectangle(A[0][2:7:4], color=GREEN, fill_opacity=0.3)
        highlight_C_11 = SurroundingRectangle(C[0][0], color=YELLOW, fill_opacity=0.3)
        c11 = MathTex(r"c_{11}").move_to(C[0][0])
        
        self.play(FadeIn(highlight_A_col))
        self.play(FadeIn(highlight_C_11))
        self.play(Transform(eq1, c11))
        self.wait(2)
        
        self.play(FadeOut(highlight_A_col), FadeOut(highlight_C_11))
    
    def repeat_for_other_elements(self):
        A, B, C = self.A, self.B, self.C
        eqs = [
            (B[0][5:7], A[0][2:7:4], C[0][1], "c_{12}", r"b_{11} \cdot a_{12} + b_{12} \cdot a_{22}"),
            (B[0][8:], A[0][2:7:4], C[0][2], "c_{21}", r"b_{21} \cdot a_{11} + b_{22} \cdot a_{21}"),
            (B[0][8:], A[0][8:], C[0][3], "c_{22}", r"b_{21} \cdot a_{12} + b_{22} \cdot a_{22}")
        ]
        for b, a, c, res, eq in eqs:
            highlight_B = SurroundingRectangle(b, color=GREEN, fill_opacity=0.3)
            highlight_A = SurroundingRectangle(a, color=GREEN, fill_opacity=0.3)
            highlight_C = SurroundingRectangle(c, color=YELLOW, fill_opacity=0.3)
            eq_tex = MathTex(eq).next_to(c, RIGHT)
            res_tex = MathTex(res).move_to(c)
            
            self.play(FadeIn(highlight_B))
            self.play(FadeIn(highlight_A))
            self.play(FadeIn(highlight_C))
            self.play(FadeIn(eq_tex))
            self.wait(2)
            self.play(Transform(eq_tex, res_tex))
            self.play(FadeOut(highlight_B), FadeOut(highlight_A), FadeOut(highlight_C))
    
    def final_result(self):
        A, B, C = self.A, self.B, self.C
        final_C = MathTex(r"C = \begin{pmatrix} c_{11} & c_{12} \\ c_{21} & c_{22} \end{pmatrix}")
        result_text = Text("Result: C = A x B").to_edge(UP)
        
        self.play(A.animate.set_opacity(0.5), B.animate.set_opacity(0.5))
        self.play(C.animate.set_color(BLUE))
        self.play(FadeIn(result_text))
        self.wait(2)
        
        self.play(FadeOut(A), FadeOut(B), FadeOut(C), FadeOut(result_text))