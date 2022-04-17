# this file contains all of the classes relevant to lines and orb movement
import pygame
from abc import ABC, abstractmethod # abstract method definition functionality
from math import sqrt

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
        self.lineEditing = None # th eline that is being placed


    def updateLines(self) -> None:
        pass


    # renders all of the lines and their orbs to the surface. needs gridOffset so lines can be panned
    def renderLines(self, window_surface: pygame.Surface, gridOffset: tuple) -> None:
        self.gridOffset = gridOffset
        for line in self.lines:
            line.renderLine(window_surface, gridOffset)


    # add line. returns true if valid placement, false if placement failed
    # if a line is currently being added to, instead adds a point to that line
    def addLine(self, pos: tuple) -> bool:
        # if there is already a line, (and not line we are editing rn) return
        overlapping = self.getLineAt(pos)
        if overlapping:
            # user clicked back on start line, finish line
            if overlapping == self.lineEditing:
                self.completeLine(pos)

            return
        

        # if there is no line being edited right now, place new line and set as line to edit.
        if self.lineEditing is None:
            line = Line(pos, self.gridOffset)
            self.lines.append(line)
            self.lineEditing = line
        # otherwise, append point to line!
        else:
            self.lineEditing.addPointFromWorldspace(pos, self.gridOffset)


    # called to complete the placement of a line
    # if pos is equal to the start pos of the line, mark the line as closed
    def completeLine(self, pos: tuple):
        startPoint = self.lineEditing.getPathScreenSpace(self.gridOffset)[0]
        if startPoint == pos:
            self.lineEditing.lineIsClosed = True

        self.lineEditing = None
    

    # checks for if a point on a line is already occupying a space
    # if performance becomes a problem, this is the culprit. Implement quadtree?
    def getLineAt(self, pos: tuple):
        # loop over all points in each line
        for line in self.lines:
            
            for point in line.getPathScreenSpace(self.gridOffset):
                # grab point x and other point x
                px, py = pos
                opx, opy = point

                # compare test pos to line point pos
                if (px < opx + COMPARE_ERROR) and (px > opx - COMPARE_ERROR):
                    if (py < opy + COMPARE_ERROR) and (py > opy - COMPARE_ERROR):
                        return line # line does overlap

        # no overlapping, return None
        return None


    # checks for if pos is between two points of any line or equal to those points
    # more expensive than getLineAt
    def getLineAtOrOver(self, pos: tuple):
        # loop over all points in each line
        for line in self.lines:
            # likely bug in current implementation: closed lines will not check for the closing segment
            prevPoint = None
            path = line.getPathScreenSpace(self.gridOffset)
            # account for last point if line is closed
            if line.lineIsClosed:
                prevPoint = path[-1]

            for point in path:
                if prevPoint is not None:
                    # since lines are clamped to horizontal and vertical only...
                    # vertical test:
                    if prevPoint[0] == point[0] == pos[0]:
                        lower = max(prevPoint[1], point[1])
                        upper = min(prevPoint[1], point[1])
                        if pos[1] <= lower and pos[1] >= upper:
                            print("vert match")

                    # horizontal test
                    if prevPoint[1] == point[1] == pos[1]:
                        right = max(prevPoint[0], point[0])
                        left =  min(prevPoint[0], point[0])
                        if pos[0] <= right and pos[0] >= left:
                            print("hot match")

                    # dsq1 = ((pos[0] - prevPoint[0])**2) + ((pos[1] - prevPoint[1])**2)
                    # dsq2 = ((point[0] - pos[0])**2) + ((point[1] - pos[1])**2)
                    # dsqLine = ((point[0] - prevPoint[0])**2) + ((point[1] - prevPoint[1])**2)

                    # print(abs((dsq1 + dsq2) - dsqLine))
                    # if abs((dsq1 + dsq2) - dsqLine) < COMPARE_ERROR:
                    #     # then the point lies between the two lines.
                    #     return Line

                # save prevPoint for next iter
                prevPoint = point


class Line:
    """
    The line class defines the points of the line, rendering, and orb movements
    """

    def __init__(self, basePos: tuple, initialGridOffset: tuple) -> None:
        self.basePoint = Point(basePos)
        self.initialGridOfset = initialGridOffset
        self.path = [] # point array
        self.orbs = [] # orb array

        # sound parameters
        self.volume = 1
        self.pitch = 1
        self.quality = 1

        self.addPoint((0, 0))
        self.lineIsClosed = False


    # moves the orbs across the line
    def update(self, delta: float):
        for orb in self.orbs:
            orb.moveTowards()


    # adds a point to the line path from a tuple
    def addPoint(self, point: tuple) -> None:
        self.path.append(Point(point))


    # adds a point from world space (used for line palcement)
    def addPointFromWorldspace(self, pos: tuple, gridOffset: tuple) -> None:
        p = self.worldToLineSpace(pos, gridOffset)
       
        self.addPoint(p)

    # adds an orb to the line path
    def addOrb(self, orb):
        self.orbs.append(orb)

    
    # renders the line to the passed surface
    def renderLine(self, window_surface: pygame.Surface, gridOffset: tuple) -> None:
        xOff, yOff = (gridOffset[0] - self.initialGridOfset[0], gridOffset[1] - self.initialGridOfset[1])

        pointsSP = self.getPathScreenSpace(gridOffset)
        if len(pointsSP) > 1:
            pygame.draw.lines(window_surface, '#00FE10', self.lineIsClosed, pointsSP, width=10)
        else:
        # temp render
            pygame.draw.circle(
                surface=window_surface, color='#00FE10', 
                center=(self.basePoint.position[0] + xOff, self.basePoint.position[1] + yOff),
                radius=10, width=0
            )

    
    def getPath(self) -> list:
        return self.path

    
    # deletes a point from the line that is at a worldspace position "pos"
    def deletePoint(self, pos: tuple, gridOffset: tuple):
        p = self.worldToLineSpace(pos, gridOffset)
        for point in self.path:
            if p == point:
                self.path.remove(point)

    # returns the path converted into screenspace coordinates as tuples (grid ofset taken into account)
    def getPathScreenSpace(self, gridOffset: tuple) -> list:
        p = []
        xOff = gridOffset[0] - self.initialGridOfset[0] + self.basePoint.position[0]
        yOff = gridOffset[1] - self.initialGridOfset[1] + self.basePoint.position[1]
        for point in self.getPath():
            p.append((point.position[0] + xOff, point.position[1] + yOff))
        
        return p


    def getBasePoint(self):
        return self.basePoint
    

    def setVolume(self, val: float):
        self.volume = val


    def setPitch(self, val: float):
        self.pitch = val


    def setQuality(self, val: float):
        self.quality = val


    # returns tuple position in line space from world space
    def worldToLineSpace(self, pos: tuple, gridOffset: tuple):
        p = (pos[0] + self.initialGridOfset[0] - gridOffset[0] - self.basePoint.position[0],
            pos[1] + self.initialGridOfset[1] - gridOffset[1] - self.basePoint.position[1])
        return p


class Orb:

    def __init__(self, start_pos: tuple, speed: float) -> None:
        self.position = start_pos
        self.speed = speed

    # moves the orb towards its next point
    def moveTowards(point, delta: float):
        pass
    

# the abstract base class for points
class AbstractPoint(ABC):
    # abstract proprty for the x component
    @property
    @abstractmethod
    def position(self):
        pass

    @position.setter
    @abstractmethod
    def position(self, val: tuple):
        pass


# represents a point on any line
class Point(AbstractPoint):
    def __init__(self, pos: tuple) -> None:
        self.position = pos

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, val: tuple):
        self._position = val

    def __str__(self) -> str:
        return f"Point: {self.position}"
    


