# this file contains all of the classes relevant to lines and orb movement


class LineManager:
    """
    The LineManager class updates lines and detects collisions with lines when they are being placed
    """
    lines = [] # array of all line class instances

    def __init__(self) -> None:
        pass


    def update_lines():
        pass



class Line:
    """
    The line class defines the points of the line, rendering, and orb movements
    """
    path = [] # the array of points
    orbs = [] # the array of attached orbs

    def __init__(self, base_pos) -> None:
        self.add_point(base_pos)


    # moves the orbs across the line
    def update(self, delta: float):
        for orb in self.orbs:
            orb.move_towards()

    # adds a point to the line path
    def add_point(self, point):
        self.path.append(point)


    # adds an orb to the line path
    def add_orb(self, orb):
        self.orbs.append(orb)


class Orb:

    def __init__(self, start_pos: tuple, speed: float) -> None:
        self.position = start_pos
        self.speed = speed

    # moves the orb towards its next point
    def move_towards(point, delta: float):
        pass
    