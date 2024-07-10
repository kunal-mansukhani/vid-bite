from manim import *

class CustomLayoutExample(Scene):
    def construct(self):
        import numpy as np
        import networkx as nx

        # create custom layout
        def custom_layout(
            graph: nx.Graph,
            scale: float | tuple[float, float, float] = 2,
            n: int | None = None,
            *args: Any,
            **kwargs: Any,
        ):
            nodes = sorted(list(graph))
            height = len(nodes) // n
            return {
                node: (scale * np.array([
                    (i % n) - (n-1)/2,
                    -(i // n) + height/2,
                    0
                ])) for i, node in enumerate(graph)
            }

        # draw graph
        n = 4
        graph = Graph(
            [i for i in range(4 * 2 - 1)],
            [(0, 1), (0, 4), (1, 2), (1, 5), (2, 3), (2, 6), (4, 5), (5, 6)],
            labels=True,
            layout=custom_layout,
            layout_config={'n': n}
        )
        self.add(graph)
class CircularLayout(Scene):
    def construct(self):
        graph = Graph(
            [1, 2, 3, 4, 5, 6],
            [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (5, 1), (1, 3), (3, 5)],
            layout="circular",
            labels=True
        )
        self.add(graph)
class KamadaKawaiLayout(Scene):
    def construct(self):
        from collections import defaultdict
        distances: dict[int, dict[int, float]] = defaultdict(dict)

        # set desired distances
        distances[1][2] = 1  # distance between vertices 1 and 2 is 1
        distances[2][3] = 1  # distance between vertices 2 and 3 is 1
        distances[3][4] = 2  # etc
        distances[4][5] = 3
        distances[5][6] = 5
        distances[6][1] = 8

        graph = Graph(
            [1, 2, 3, 4, 5, 6],
            [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1)],
            layout="kamada_kawai",
            layout_config={"dist": distances},
            layout_scale=4,
            labels=True
        )
        self.add(graph)
class PartiteLayout(Scene):
    def construct(self):
        graph = Graph(
            [1, 2, 3, 4, 5, 6],
            [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (5, 1), (1, 3), (3, 5)],
            layout="partite",
            layout_config={"partitions": [[1,2],[3,4],[5,6]]},
            labels=True
        )
        self.add(graph)

class PlanarLayout(Scene):
    def construct(self):
        graph = Graph(
            [1, 2, 3, 4, 5, 6],
            [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (5, 1), (1, 3), (3, 5)],
            layout="planar",
            layout_scale=4,
            labels=True
        )
        self.add(graph)
    
class RandomLayout(Scene):
    def construct(self):
        graph = Graph(
            [1, 2, 3, 4, 5, 6],
            [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (5, 1), (1, 3), (3, 5)],
            layout="random",
            labels=True
        )
        self.add(graph)
class ShellLayout(Scene):
    def construct(self):
        nlist = [[1, 2, 3], [4, 5, 6, 7, 8, 9]]
        graph = Graph(
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [(1, 2), (2, 3), (3, 1), (4, 1), (4, 2), (5, 2), (6, 2), (6, 3), (7, 3), (8, 3), (8, 1), (9, 1)],
            layout="shell",
            layout_config={"nlist": nlist},
            labels=True
        )
        self.add(graph)
    
class SpectralLayout(Scene):
    def construct(self):
        graph = Graph(
            [1, 2, 3, 4, 5, 6],
            [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (5, 1), (1, 3), (3, 5)],
            layout="spectral",
            labels=True
        )
        self.add(graph)
class SpiralLayout(Scene):
    def construct(self):
        graph = Graph(
            [1, 2, 3, 4, 5, 6],
            [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (5, 1), (1, 3), (3, 5)],
            layout="spiral",
            labels=True
        )
        self.add(graph)


class SpringLayout(Scene):
    def construct(self):
        graph = Graph(
            [1, 2, 3, 4, 5, 6],
            [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (5, 1), (1, 3), (3, 5)],
            layout="spring",
            labels=True
        )
        self.add(graph)
class TreeLayout(Scene):
    def construct(self):
        graph = Graph(
            [1, 2, 3, 4, 5, 6, 7],
            [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
            layout="tree",
            layout_config={"root_vertex": 1},
            labels=True
        )
        self.add(graph)