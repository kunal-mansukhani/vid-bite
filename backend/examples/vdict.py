from manim import *

class ShapesWithVDict(Scene):
    def construct(self):
        square = Square().set_color(RED)
        circle = Circle().set_color(YELLOW).next_to(square, UP)

        # create dict from list of tuples each having key-mobject pair
        pairs = [("s", square), ("c", circle)]
        my_dict = VDict(pairs, show_keys=True)

        # display it just like a VGroup
        self.play(Create(my_dict))
        self.wait()

        text = Tex("Some text").set_color(GREEN).next_to(square, DOWN)

        # add a key-value pair by wrapping it in a single-element list of tuple
        # after attrs branch is merged, it will be easier like `.add(t=text)`
        my_dict.add([("t", text)])
        self.wait()

        rect = Rectangle().next_to(text, DOWN)
        # can also do key assignment like a python dict
        my_dict["r"] = rect

        # access submobjects like a python dict
        my_dict["t"].set_color(PURPLE)
        self.play(my_dict["t"].animate.scale(3))
        self.wait()

        # also supports python dict styled reassignment
        my_dict["t"] = Tex("Some other text").set_color(BLUE)
        self.wait()

        # remove submobject by key
        my_dict.remove("t")
        self.wait()

        self.play(Uncreate(my_dict["s"]))
        self.wait()

        self.play(FadeOut(my_dict["c"]))
        self.wait()

        self.play(FadeOut(my_dict["r"], shift=DOWN))
        self.wait()

        # you can also make a VDict from an existing dict of mobjects
        plain_dict = {
            1: Integer(1).shift(DOWN),
            2: Integer(2).shift(2 * DOWN),
            3: Integer(3).shift(3 * DOWN),
        }

        vdict_from_plain_dict = VDict(plain_dict)
        vdict_from_plain_dict.shift(1.5 * (UP + LEFT))
        self.play(Create(vdict_from_plain_dict))

        # you can even use zip
        vdict_using_zip = VDict(zip(["s", "c", "r"], [Square(), Circle(), Rectangle()]))
        vdict_using_zip.shift(1.5 * RIGHT)
        self.play(Create(vdict_using_zip))
        self.wait()