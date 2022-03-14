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
        self.dotList = [] # List of dots. This will be used to test if lines are valid when they are being drawn. 
        
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