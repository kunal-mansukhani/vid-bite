from manim import *

class LSTMAnimation(Scene):
    def construct(self):
        self.s1()
        c,f,i,o,t = self.s2()
        id,ia = self.s3(i)
        fa = self.s4(f)
        oa = self.s5(o)
        cu = self.s6(c)
        op = self.s7(o)
        self.s8(c,f,i,o,t,id,ia,fa,oa,cu,op)

    def s1(self):
        t = Text("Long Short-Term Memory (LSTM)",font_size=40)
        self.play(FadeIn(t))
        self.wait(1)
        self.play(FadeOut(t))

    def s2(self):
        c = Rectangle(height=1,width=4).move_to([0,0,0])
        f = Rectangle(height=1,width=1).move_to([-2,-1.5,0])
        i = Rectangle(height=1,width=1).move_to([0,-1.5,0])
        o = Rectangle(height=1,width=1).move_to([2,-1.5,0])
        t = VGroup(
            MathTex("C").next_to(c,UP),
            MathTex("f").next_to(f,UP),
            MathTex("i").next_to(i,UP),
            MathTex("o").next_to(o,UP)
        )
        sg = VGroup(Circle(radius=0.2).move_to(f),Circle(radius=0.2).move_to(i),Circle(radius=0.2).move_to(o))
        self.play(Create(c),Create(f),Create(i),Create(o),Write(t),Create(sg))
        return c,f,i,o,t

    def s3(self,i):
        id = Dot().move_to([-3,-1.5,0])
        ia = Arrow(id.get_center(),i.get_left(),buff=0.1)
        it = Text("Input Data",font_size=20).next_to(id,DOWN)
        self.play(Create(id),GrowArrow(ia))
        self.play(i.animate.set_fill(YELLOW,opacity=0.5),Write(it))
        return id,ia

    def s4(self,f):
        ft = Text("Forget Gate Active",font_size=20).next_to(f,DOWN)
        self.play(f.animate.set_fill(GREEN,opacity=0.5),Write(ft))
        return f

    def s5(self,o):
        ot = Text("Output Gate Active",font_size=20).next_to(o,DOWN)
        self.play(o.animate.set_fill(RED,opacity=0.5),Write(ot))
        return o

    def s6(self,c):
        ct = Text("Cell State Updated",font_size=20).next_to(c,DOWN)
        self.play(c.animate.set_fill(BLUE,opacity=0.5),Write(ct))
        return c

    def s7(self,o):
        op = Dot().move_to([3,-1.5,0])
        oa = Arrow(o.get_right(),op.get_center(),buff=0.1)
        ot = Text("Output",font_size=20).next_to(op,DOWN)
        self.play(Create(op),GrowArrow(oa),Write(ot))
        return op

    def s8(self,c,f,i,o,t,id,ia,fa,oa,cu,op):
        g = VGroup(c,f,i,o,t,id,ia,fa,oa,cu,op)
        tx = Text("LSTM Cell",font_size=40).next_to(g,DOWN)
        self.play(Write(tx))
        self.wait(1)
        self.play(FadeOut(g),FadeOut(tx))

