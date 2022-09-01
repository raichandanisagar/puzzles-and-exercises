import numpy as np
from matplotlib.pyplot import plot, scatter


class Spider:
    """Simulate how a spider walks"""

    def __init__(self, x=0, y=0):
        """Initialize spider instance with coordinates (position) x & y zero (default)"""
        self._x = x
        self._y = y
        self._path = [(self._x, self._y)]

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def path(self):
        return self._path

    def next_move(self):
        """A move invovles picking an angle (0-360 degrees or 2pi radians)
        and a certain distance (between 1 and 2m) and calculating subsequent x and y"""

        move_angle = np.random.uniform(0, 2 * np.pi)
        move_distance = np.random.uniform(0, 2)

        self._x += move_distance * np.sin(move_angle)
        self._y += move_distance * np.cos(move_angle)
        self._path.append((self.x, self.y))

    def position_check(self, xlim, ylim):
        """Returns True if spider is in the designated area.
        xlim -> tuple of (xmin, xmax)
        ylim -> tuple of (ymin, ymax)"""

        return (xlim[0] <= self.x <= xlim[1]) and (ylim[0] <= self.y <= ylim[1])

    def plot_path(self):
        spider_xpath = [pos[0] for pos in self.path]
        spider_ypath = [pos[1] for pos in self.path]
        plot(spider_xpath, spider_ypath, 'go--', linewidth=1, markersize=2)


if __name__ == '__main__':
    sim = 1000
    iter_per_sim = 240
    sim_results = {}

    for i in range(sim):
        s = Spider()

        # default assumption that spider is not in designated area
        position_check = s.position_check(xlim=(10, 15), ylim=(6, 10))
        sim_results[i] = {'steps': None, 'position_check': position_check}

        for iter in range(iter_per_sim):
            s.next_move()
            position_check = s.position_check(xlim=(10, 15), ylim=(6, 10))
            # sim_results[i]['iteration'][iter] = {'pos': (s.x, s.y), 'position_check': position_check}
            if position_check:
                break

        position_check = s.position_check(xlim=(10, 15), ylim=(6, 10))
        sim_results[i]['position_check'] = position_check
        sim_results[i]['path'] = s.path
        sim_results[i]['steps'] = iter
