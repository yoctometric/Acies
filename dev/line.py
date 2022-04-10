# this file contains all of the classes relevant to lines and orb movement
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
    

    # checks for if a line is already occupying a space
    # if performance becomes a problem, this is the culprit. Implement quadtree?
    def getLineAt(self, pos: tuple):
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


    # adds a point to the line path
    def addPoint(self, point: tuple) -> None:
        self.path.append(point)


    # adds a point from world space (used for line palcement)
    def addPointFromWorldspace(self, pos: tuple, gridOffset: tuple) -> None:
        p = (pos[0] + self.initialGridOfset[0] - gridOffset[0] - self.basePos[0],
            pos[1] + self.initialGridOfset[1] - gridOffset[1] - self.basePos[1])
       
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
    

    def setVolume(self, val: float):
        self.volume = val


    def setPitch(self, val: float):
        self.pitch = val


    def setQuality(self, val: float):
        self.quality = val


class Orb:

    def __init__(self, start_pos: tuple, speed: float) -> None:
        self.position = start_pos
        self.speed = speed

    # moves the orb towards its next point
    def moveTowards(point, delta: float):
        pass
    