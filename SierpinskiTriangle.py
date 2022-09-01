from matplotlib import pyplot as plt
import numpy as np


class Point:
    """A class for points on a 2d plane"""

    def __init__(self, x=0, y=0):
        self._x, self._y = x, y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __repr__(self):
        return f'{self.x},{self.y}'

    def __mul__(self, realnum):
        """Multiply a point with a real number"""
        if isinstance(realnum, (int, float)):
            return Point(realnum * self.x, realnum * self.y)
        elif isinstance(realnum, Point):
            return Point(self.x * realnum.x, self.y * realnum.y)
        else:
            raise ValueError("Expected numeric or Point instance")

    def __rmul__(self, realnum):
        return self.__mul__(realnum)

    def __add__(self, other):
        """Add a Point to another Point"""
        return Point(self.x + other.x, self.y + other.y)

    def distance(self, other):
        return np.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def midpoint(self, other):
        return Point((self.x + other.x) / 2, (self.y + other.y) / 2)

    def plot(self):
        return plt.scatter(self.x, self.y, s=5, marker='o')


class Triangle:
    """A class for triangle objects"""

    def __init__(self, vertices=[Point(0, 0), Point(1, 0), Point(0, 1)]):
        """A triangle defined by 3 vertices-- each vertex is a Point object"""

        if isinstance(vertices, list):
            if not all(isinstance(point, Point) for point in vertices):
                raise TypeError("Expected each vertex to be of Point class")
            if len(vertices) != 3:
                raise ValueError(f"Expected 3 vertices; received {len(vertices)}")
        else:
            raise TypeError("vertices arg is expected to a list of Points")

        self._vertices = vertices
        self._points = vertices.copy()

    @property
    def vertices(self):
        return self._vertices

    @property
    def vertices_x(self):
        return [vertex.x for vertex in self.vertices]

    def vertices_y(self):
        return [vertex.y for vertex in self.vertices]

    @property
    def points(self):
        return self._points

    @property
    def points_x(self):
        return [point.x for point in self.points]

    @property
    def points_y(self):
        return [point.y for point in self.points]

    def draw(self):
        """Draw a scatter plot of the triangle (interior points and vertices)"""
        plt.scatter(self.points_x, self.points_y, s=2, marker='x')

    def rand_interior(self):
        """A random point interior to the triangle's points"""
        r1 = np.random.rand()
        r2 = np.random.rand()
        p = (1 - np.sqrt(r1)) * self._vertices[0] + (np.sqrt(r1) * (1 - r2)) * self._vertices[1] + \
            (r2 * np.sqrt(r1)) * self._vertices[2]
        return p

    def draw_sierpinski(self, n=1000):
        seed = self.rand_interior()  # first random point to get the process started
        self.points.append(seed)

        for i in range(n):
            random_vertex = np.random.choice(self.vertices)
            seed_midpoint = random_vertex.midpoint(seed)
            self.points.append(seed_midpoint)
            seed = seed_midpoint

        self.draw()

