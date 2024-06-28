from manim import *

class TV(ThreeDScene):
    def construct(self):
        self.s1()
        self.s2()
        self.s3()
        self.s4()
        self.s5()

    def s1(self):
        sq=VGroup(*[Square(.5,fill_opacity=.8)for _ in range(5)])
        sq.arrange(RIGHT,buff=.2).move_to(ORIGIN)
        cl=[RED,BLUE,GREEN,YELLOW,PURPLE]
        for i,s in enumerate(sq):
            s.set_fill(cl[i])
            s.add(Text(chr(65+i),font_size=24).move_to(s))
        t=Text("Input Sequence",font_size=36).next_to(sq,UP)
        self.play(FadeIn(sq,t))
        self.wait(1)
        self.play(FadeOut(sq,t))

    def s2(self):
        self.set_camera_orientation(phi=75*DEGREES,theta=-30*DEGREES)
        ax=ThreeDAxes()
        d=[Dot3D(point=[np.random.uniform(-3,3)for _ in range(3)],color=c)
           for c in [RED,BLUE,GREEN,YELLOW,PURPLE]]
        t=Text("Embedding Layer",font_size=36).to_edge(DOWN)
        self.play(Create(ax),*[FadeIn(dot)for dot in d],Write(t))
        self.wait(1)
        self.play(FadeOut(ax,*d))
        self.move_camera(phi=0,theta=-90*DEGREES)

    def s3(self):
        d=[Dot(point=[np.random.uniform(-3,3)for _ in range(2)]+[0])
           for _ in range(5)]
        l=VGroup(*[Line(d[i].get_center(),d[j].get_center(),stroke_width=2)
                   for i in range(5)for j in range(5)if i!=j])
        c=[RED,BLUE,GREEN]
        for i,line in enumerate(l):
            line.set_color(c[i%3])
        t=Text("Attention Mechanism",font_size=36).to_edge(UP)
        self.play(*[FadeIn(dot)for dot in d],Write(t))
        self.play(Create(l))
        self.play(*[dot.animate.shift(RIGHT*.1)for dot in d])
        self.wait(1)
        self.play(FadeOut(l))
        return VGroup(*d)

    def s4(self):
        d=VGroup(*[Dot()for _ in range(5)])
        d.arrange_in_grid(rows=1,cols=5,buff=.5)
        r=VGroup(*[Rectangle(height=.5,width=2.5)for _ in range(3)])
        r.arrange(UP,buff=.2).next_to(d,UP)
        t=Text("Feedforward Network",font_size=36).to_edge(DOWN)
        self.play(FadeIn(d,r,t))
        self.play(*[dot.animate.move_to(dot.get_center()+
                   np.array([np.random.uniform(-.1,.1),
                             np.random.uniform(-.1,.1),0]))
                    for dot in d])
        self.wait(1)
        self.play(FadeOut(r,t))
        return d

    def s5(self):
        sq=VGroup(*[Square(.5,fill_opacity=.8)for _ in range(5)])
        sq.arrange(RIGHT,buff=.2).move_to(ORIGIN)
        cl=[ORANGE,TEAL,PINK,MAROON,GOLD]
        for i,s in enumerate(sq):
            s.set_fill(cl[i])
        t=Text("Output Sequence",font_size=36).to_edge(UP)
        self.play(ReplacementTransform(self.s4(),sq),Write(t))
        self.wait(1)
        self.play(FadeOut(sq,t))