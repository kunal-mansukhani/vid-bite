from manim import *

class DodecahedronScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        obj = Dodecahedron()
        self.add(obj)
class IcosahedronScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        obj = Icosahedron()
        self.add(obj)

class OctahedronScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        obj = Octahedron()
        self.add(obj)
class SquarePyramidScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        vertex_coords = [
            [1, 1, 0],
            [1, -1, 0],
            [-1, -1, 0],
            [-1, 1, 0],
            [0, 0, 2]
        ]
        faces_list = [
            [0, 1, 4],
            [1, 2, 4],
            [2, 3, 4],
            [3, 0, 4],
            [0, 1, 2, 3]
        ]
        pyramid = Polyhedron(vertex_coords, faces_list)
        self.add(pyramid)
class PolyhedronSubMobjects(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        octahedron = Octahedron(edge_length = 3)
        octahedron.graph[0].set_color(RED)
        octahedron.faces[2].set_color(YELLOW)
        self.add(octahedron)
class TetrahedronScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        obj = Tetrahedron()
        self.add(obj)