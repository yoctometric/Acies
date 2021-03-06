# FOR UNIT TESTS commented lines 91 and 141
# this file contains all of the classes relevant to lines and orb movement
import pygame
from abc import ABC, abstractmethod # abstract method definition functionality
from math import sqrt
import inspect

# the error value used when == comparing floating point positions
COMPARE_ERROR = 0.01

# unused
import enum
class X_and_Y(enum.Enum):
  x = 1
  y = 2
  
"""
    Structure:
    LineManager.lines[]
        Line.path[]
            Point.position (tuple)
        Line.orbs[]
            Orb.position (tuple)
            Orb.speed (float)
"""

class LineManager:
    """
    The LineManager class updates lines and detects collisions with lines when they are being placed
    """

    def __init__(self, screenDimensions: tuple) -> None:
        self.lines = []
        self.gridOffset = (0, 0) # set in render call, taken from grid
        self.screenDimensions = screenDimensions # mostly stored for tool actions
        self.lineEditing = None # the line that is being placed
        self.prevPos = None # the point on the grid that is being edited

    def setLineEditing(self, line):
        # print("Line Editing Set to " + str(line) + "called by " + inspect.stack()[1][3])
        self.lineEditing = line
        return 0

    def getLineEditing(self):
        return self.lineEditing

    def updateLines(self) -> None:
        pass


    # renders all of the lines and their orbs to the surface. needs gridOffset so lines can be panned
    def renderLines(self, window_surface: pygame.Surface, gridOffset: tuple) -> None:
        self.gridOffset = gridOffset
        for line in self.lines:
            line.renderLine(window_surface, gridOffset)

    # determine if a line would cross an existing line, ***currently NOT WORKING, in-progress!***
    def crosses(self, prev:tuple, curr:tuple) -> bool:
        # print("Prev: " + str(prev))
        # print("Curr: " + str(curr))
        for line in self.lines:
            for i in range(len(line.path)-1):
                """
                'i' and 'j' are arbitrary names of existing points

                line.path[i].position[0]      = i[x]    existing point i x-coordinate
                line.path[i].position[1]      = i[y]    existing point i y-coordinate
                line.path[i+1].position[0]    = j[x]    existing point j x-coordinate
                line.path[i+1].position[1]    = j[y]    existing point j y-coordinate
                prev[0]                       = prev[x] previously placed point x-coordinate
                prev[1]                       = prev[y] previously placed point y-coordinate
                curr[0]                       = pos[x]  newly placed point x-coordinate
                curr[1]                       = pos[y]  newly placed point y-coordinate
                """

                if curr[0] == prev[0]: # if proposed line is vertical
                    # print("Clicked line is vertical!")
                    if (curr[0] >= line.path[i].position[0] and curr[0] <= line.path[i+1].position[0]) \
                        or (curr[0] <= line.path[i].position[0] and curr[0] >= line.path[i+1].position[0]):
                        # clicked line is vertically between existing points
                        if (prev[1] <= line.path[i].position[1] and curr[1] >= line.path[i].position[1]) \
                            or (prev[1] >= line.path[i].position[1] and curr[1] <= line.path[i].position[1]):
                            # clicked line horizontally coincides with the existing line
                            # print("Overlaps an existing vertical line!")
                            return True

                elif curr[1] == prev[1]: # if proposed line is horizontal
                    # print("Clicked line is horizontal!")
                    if (curr[1] >= line.path[i].position[1] and curr[1] <= line.path[i+1].position[1]) \
                        or (curr[1] <= line.path[i].position[1] and curr[1] >= line.path[i+1].position[1]):
                        # clicked line is horizontally between existing points
                        if (prev[0] <= line.path[i].position[0] and curr[0] >= line.path[i].position[0]) \
                            or (prev[0] >= line.path[i].position[0] and curr[0] <= line.path[i].position[0]):
                            # clicked line vertically coincides with the existing line
                            # print("Overlaps an existing horizontal line!")
                            return True

                else:
                    pass
                    # print("Error: line is diagonal, somehow reached crosses().")

                # TODO: determine if a line would cross (overlap, just not on endpoints, on actual line)
                #   if it is in the *same* direction as an existing line

        # print("Doesn't cross!")
        return False # once all of the lines have been checked and no crosses exist


    # add line. returns true if valid placement, false if placement failed
    # if a line is currently being added to, instead adds a point to that line
    
    def addLine(self, pos: tuple) -> bool:
        # print("Line editing: " + str(self.lineEditing))
        # print("PrevPos: " + str(self.prevPos))
        # if there is already a line, (and not line we are editing rn) return
        overlapping = self.getLineAt(pos)
        # if overlapping and not diagonal
        if overlapping and (self.prevPos[0] == pos[0] or self.prevPos[1] == pos[1]): 
            # user clicked back on start line, finish and complete line
            if overlapping == self.lineEditing:
                self.completeLine(pos)

        elif overlapping and not (self.prevPos[0] == pos[0] or self.prevPos[1] == pos[1]): 
            # user clicked back on start line
            if overlapping == self.lineEditing:
                self.setLineEditing(None)
        
        # if there is no line being edited right now, place new line and set as line to edit.
        elif self.lineEditing is None:
            # print("LineEditing is none")
            line = Line(pos, self.gridOffset)
            self.lines.append(line)
            self.prevPos = pos
            # print("PrevPos assigned: " + str(self.prevPos))
            self.setLineEditing(line)
            return 0

        # if the new point wouldn't be diagonal AND if the new line wouldn't overlap, then append point to line
        elif (self.prevPos[0] == pos[0] or self.prevPos[1] == pos[1]) and not\
            self.crosses(self.prevPos,pos):
            self.lineEditing.addPointFromWorldspace(pos, self.gridOffset)
            self.prevPos = pos
            return 0

        else:
            # print("Tried to place a diagonal or crossed line.")
            return -1


    # called to complete the placement of a line
    # if pos is equal to the start pos of the line, mark the line as closed
    def completeLine(self, pos: tuple, testing:bool = None) -> int:
        startPoint = self.lineEditing.getPathScreenSpace(self.gridOffset)[0]
        if startPoint == pos:
            self.lineEditing.lineIsClosed = True
            flag = 0
        else:
            flag = -1
        self.setLineEditing(None)
        return flag
    

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
                            return line

                    # horizontal test
                    if prevPoint[1] == point[1] == pos[1]:
                        right = max(prevPoint[0], point[0])
                        left =  min(prevPoint[0], point[0])
                        if pos[0] <= right and pos[0] >= left:
                            return line

                # save prevPoint for next iter
                prevPoint = point

        # no line found
        return None



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
        assert type(point) == tuple
        self.path.append(Point(point))


    # adds a point from world space (used for line palcement)
    def addPointFromWorldspace(self, pos: tuple, gridOffset: tuple) -> None:
        p = self.worldToLineSpace(pos, gridOffset)
       
        self.addPoint(p)

    # adds an orb to the line path
    def addOrb(self, screenPos: tuple, gridOffset: tuple):
        orb = Orb(self.worldToLineSpace(screenPos, gridOffset),0)

        self.orbs.append(orb)

    
    # renders the line to the passed surface
    def renderLine(self, window_surface: pygame.Surface, gridOffset: tuple) -> None:
        xOff, yOff = (gridOffset[0] - self.initialGridOfset[0], gridOffset[1] - self.initialGridOfset[1])

        pointsSP = self.getPathScreenSpace(gridOffset)
        if len(pointsSP) > 1:
            pygame.draw.lines(window_surface, '#00FE10', self.lineIsClosed, pointsSP, width=10)
        else:
            pygame.draw.circle(
                surface=window_surface, color='#00FE10', 
                center=(self.basePoint.position[0] + xOff, self.basePoint.position[1] + yOff),
                radius=10, width=0
            )
        
        # draw all orbs
        for o in self.orbs:
            pygame.draw.circle(
                surface=window_surface, color='#000000', 
                center=self.lineToWorldSpace(o.position, gridOffset),
                radius=10, width=0
            )

    
    def getPath(self) -> list:
        return self.path

    
    # deletes a point from the line that is at a worldspace position "pos"
    def deletePoint(self, pos: tuple, gridOffset: tuple) -> bool:
        p = self.worldToLineSpace(pos, gridOffset)
        for point in self.path:
            if p == point.position:
                self.path.remove(point)
                return True
        
        return False


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
    
    # returns tuple position in world space from line space
    def lineToWorldSpace(self, pos: tuple, gridOffset: tuple):
        p = (pos[0] + gridOffset[0] - self.initialGridOfset[0] + self.basePoint.position[0],
            pos[1] + gridOffset[1] - self.initialGridOfset[1] + self.basePoint.position[1])
        return p

    # in the future, if we decide to be able to drag and move lines
    def move(delta:tuple) -> None:
        pass


# the abstract base class (ABC) for Points and Orbs
class LineMember(ABC):
    def __init__(self, pos:tuple):
        self.position = pos

    @abstractmethod
    def getPosition(self):
        pass

    @abstractmethod
    def move(self,delta:tuple):
        pass

    @abstractmethod
    def delete(self):
        pass


# concrete class of Point, represents a point on any line
class Point(LineMember):
    def __init__(self, pos:tuple) -> None:
        super().__init__(pos)
        self.position = pos
    
    def getPosition(self):
        return self.position

    # for future capabilities of dragging and moving lines as a whole
    def move(self,delta:tuple):
        self.position[0] += delta[0]
        self.position[1] += delta[1]

    def delete(self):
        self.position = (-1,-1)

    def __str__(self) -> str:
        return f"Point: {self.position}"


# concrete class of Orb, represents an orb on any line
class Orb(LineMember):

    def __init__(self, start_pos:tuple, speed:float) -> None:
        self.position = start_pos
        self.speed = speed

    def getPosition(self):
        return self.position

    # for future capabilities of dragging and moving lines as a whole
    def move(self,delta:tuple):
        self.position[0] += delta[0]
        self.position[1] += delta[1]

    def delete(self):
        self.position = (-1,-1)

    # moves the orb towards its next point
    def travelTowards(point:tuple, delta: float):
        pass
