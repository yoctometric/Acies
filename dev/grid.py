#Creates grid for Acies
#File intended to be used as a Module

import pygame

pygame.init()

# Purpose: to only allow valid intersections.
# If this goes against our architecture then we can delete.
class Dot:
    def __init__(self, x, y, numInhabited = 0):
        self.x = x
        self.y = y
        self.numInhabited = numInhabited

    def getNumInhabited(self):
        return self.numInhabited


# Creates grid
class Grid:
    def __init__(self, width, height, numColumns, numRows, buffer=8):
        self.columnPoints = []
        self.rowPoints = []
        self.points = [self.columnPoints, self.rowPoints]
        self.buffer = buffer
        self.dotList = [] # 2d array of dots
        
        for i in range(numColumns + 1):  
            self.columnPoints.append(self.buffer + i * int((width - 2 * self.buffer) / (numColumns -1)))

        for i in range(numRows + 1):
            self.rowPoints.append(self.buffer + i * int((height - 2 * self.buffer) / (numRows -1)))
            
        for i in range(len(self.columnPoints)):
            self.dotList.append([])
            for k in range(len(self.rowPoints)):
                self.dotList[i].append(Dot(i,k)) # adds dot objects to dotList


    def drawGrid(self, window_surface):
        self.totalPoints = len(self.columnPoints) * len(self.rowPoints)

        for i in range(len(self.columnPoints)):
            for k in range(len(self.rowPoints)):
                pygame.draw.rect(window_surface, '#000000', (self.points[0][i], self.points[1][k], 4, 4), 0) # visually creates rectangles on grid


    def getRows(self):
        return self.rowPoints

    def getColumns(self):
        return self.columnPoints

    def getPoints(self):
        return self.points

    def getDots(self):
        return self.dotList



class ResizableGrid:
    """
    A grid defined by point spacing, offset, and screen dimensions. 
    This allows the grid to be updated in scale and moved.

    The grid has no concept of an actual point, and does not store any in memory. This is what will
    hopefully allow the grid to be panned and scaled infinitely without disasterous memory affects.
    It also means that the LineManager will have to handle all of the placement and collision detection,
    but it can be hooked to the grid so that when the grid is scaled it moves the lines appropriately.
    """
    def __init__(self, pointSpacing: float, pointSize: float, gridOffset: tuple, screenDimensions: tuple) -> None:
        self.update(pointSpacing, pointSize, gridOffset, screenDimensions)


    # updates the values of the grid, redefining its size and shape
    def update(self, pointSpacing: float, pointSize: float, gridOffset: tuple, screenDimensions: tuple):
        self.pointSpacing = pointSpacing
        self.pointSize = pointSize
        self.gridOffset = gridOffset
        self.screenDimensions = screenDimensions

        # find left edge of grid to render
        xOffset, yOffset = gridOffset
        xEdge = (xOffset % pointSpacing) - pointSpacing
        yEdge = (yOffset % pointSpacing) - pointSpacing

        # find num points to render in each axis
        xNumPoints = (screenDimensions[0] // pointSpacing) + 1
        yNumPoints = (screenDimensions[1] // pointSpacing) + 1

        # keep track of these values so rendering doesn't need to calculate them each time
        self.renderEdges = (xEdge, yEdge)
        self.renderPointCounts = (xNumPoints, yNumPoints)


    # pans the grid by <difference> pixels.
    def panGrid(self, difference: tuple) -> None:
        offset = (self.gridOffset[0] + difference[0], self.gridOffset[1] + difference[1])
        self.update(self.pointSpacing, self.pointSize, offset, self.screenDimensions)

    
    # zooms the grid by <scale>
    def zoomGrid(self, scale: float):
        pass


    # draws the grid to the surface
    def drawGrid(self, window_surface: pygame.Surface):
        for x in range(self.renderPointCounts[0]):
            for y in range(self.renderPointCounts[1]):
                # draw a circle at the calculated point position
                pygame.draw.circle(
                    surface=window_surface, color='#000000', 
                    center=(x * self.pointSpacing + self.renderEdges[0], y * self.pointSpacing + self.renderEdges[1]),
                    radius=self.pointSize, width=0
                )

    
    # takes in a position and rounds it to the exact location of a dot. Used for snapping to grid
    def getNearestPosition(self, pos: tuple) -> tuple:
        xPos, yPos = pos

        xMod = xPos % self.pointSpacing
        yMod = yPos % self.pointSpacing

        newXPos = -1
        newYPos = -1


        # get the four bounds around the position
        left = xPos - xMod + self.renderEdges[0] + self.pointSpacing
        right = xPos + xMod + self.renderEdges[0] + self.pointSpacing
        top = yPos - yMod + self.renderEdges[1] + self.pointSpacing
        bottom = yPos + yMod + self.renderEdges[1] + self.pointSpacing

        # round x
        if xPos > (left + right) / 2:
            newXPos = right
        else:
            newXPos = left

        # round y
        if yPos > (top + bottom) / 2:
            newYPos = bottom
        else:
            newYPos = top

        return (newXPos, newYPos)
    

    def getGridOffset(self) -> tuple:
        return self.gridOffset