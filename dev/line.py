# this file contains all of the classes relevant to lines and orb movement
from email.mime import base
from matplotlib.pyplot import grid
import pygame

class LineManager:
    """
    The LineManager class updates lines and detects collisions with lines when they are being placed
    """

    def __init__(self) -> None:
        self.lines = []
        self.gridOffset = (0, 0) # set in render call, taken from grid


    def updateLines(self) -> None:
        pass


    # renders all of the lines and their orbs to the surface. needs gridOffset so lines can be panned
    def renderLines(self, window_surface: pygame.Surface, gridOffset: tuple) -> None:
        self.gridOffset = gridOffset
        for line in self.lines:
            line.renderLine(window_surface, gridOffset)


    # add line. returns true if valid placement, false if placement failed
    def addLine(self, pos: tuple) -> bool:
        line = Line(pos, self.gridOffset)
        self.lines.append(line)
    

    # checks for if a line is already occupying a space
    def lineOverlaps(self, pos: tuple) -> bool:
        for line in self.lines:
            pass
        # TODO: implement



class Line:
    """
    The line class defines the points of the line, rendering, and orb movements
    """

    def __init__(self, base_pos: tuple, initialGridOffset: tuple) -> None:
        self.base_pos = base_pos
        self.initialGridOfset = initialGridOffset
        self.path = [] # point array
        self.orbs = [] # orb array

        self.addPoint((0, 0))


    # moves the orbs across the line
    def update(self, delta: float):
        for orb in self.orbs:
            orb.moveTowards()


    # adds a point to the line path
    def addPoint(self, point):
        self.path.append(point)


    # adds an orb to the line path
    def addOrb(self, orb):
        self.orbs.append(orb)

    
    # renders the line to the passed surface
    def renderLine(self, window_surface: pygame.Surface, gridOffset: tuple) -> None:
        xOff, yOff = (gridOffset[0] - self.initialGridOfset[0], gridOffset[1] - self.initialGridOfset[1])

        # temp render
        pygame.draw.circle(
            surface=window_surface, color='#00FE10', 
            center=(self.base_pos[0] + xOff, self.base_pos[1] + yOff),
            radius=10, width=0
        )



class Orb:

    def __init__(self, start_pos: tuple, speed: float) -> None:
        self.position = start_pos
        self.speed = speed

    # moves the orb towards its next point
    def moveTowards(point, delta: float):
        pass
    