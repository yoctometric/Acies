# this file contains all of the classes relevant to lines and orb movement
from email.mime import base
from matplotlib.pyplot import grid
import pygame


# the error value used when == comparing floating point positions
COMPARE_ERROR = 0.01


class LineManager:
    """
    The LineManager class updates lines and detects collisions with lines when they are being placed
    """

    def __init__(self, screenDimensions: tuple) -> None:
        self.lines = []
        self.gridOffset = (0, 0) # set in render call, taken from grid
        self.screenDimensions = screenDimensions # mostly stored for tool actions


    def updateLines(self) -> None:
        pass


    # renders all of the lines and their orbs to the surface. needs gridOffset so lines can be panned
    def renderLines(self, window_surface: pygame.Surface, gridOffset: tuple) -> None:
        self.gridOffset = gridOffset
        for line in self.lines:
            line.renderLine(window_surface, gridOffset)


    # add line. returns true if valid placement, false if placement failed
    def addLine(self, pos: tuple) -> bool:
        # if there is already a line, return
        if self.getLineAt(pos):
            return
        
        line = Line(pos, self.gridOffset)
        self.lines.append(line)
    

    # checks for if a line is already occupying a space
    # if performance becomes a problem, this is the culprit. Implement quadtree?
    def getLineAt(self, pos: tuple) -> bool:
        # loop over all points in each line
        for line in self.lines:
            for point in line.getPathScreenSpace(self.gridOffset):
                px, py = pos
                opx, opy = point

                # compare test pos to line point pos
                if (px < opx + COMPARE_ERROR) and (px > opx - COMPARE_ERROR):
                    if (py < opy + COMPARE_ERROR) and (py > opy - COMPARE_ERROR):
                        return line # line does overlap

        # no overlapping, return None
        return None



class Line:
    """
    The line class defines the points of the line, rendering, and orb movements
    """

    def __init__(self, basePos: tuple, initialGridOffset: tuple) -> None:
        self.basePos = basePos
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
            center=(self.basePos[0] + xOff, self.basePos[1] + yOff),
            radius=10, width=0
        )

    
    def getPath(self) -> list:
        return self.path
    

    # returns the path converted into screenspace coordinates (grid ofset taken into account)
    def getPathScreenSpace(self, gridOffset: tuple) -> list:
        p = []
        xOff = gridOffset[0] - self.initialGridOfset[0] + self.basePos[0]
        yOff = gridOffset[1] - self.initialGridOfset[1] + self.basePos[1]
        for point in self.getPath():
            p.append((point[0] + xOff, point[1] + yOff))
        
        return p


    def getBasePos(self) -> tuple:
        return self.basePos



class Orb:

    def __init__(self, start_pos: tuple, speed: float) -> None:
        self.position = start_pos
        self.speed = speed

    # moves the orb towards its next point
    def moveTowards(point, delta: float):
        pass
    