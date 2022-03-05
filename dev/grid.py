#Creates grid for Acies
#File intended to be used as a Module

import pygame

pygame.init()

#Creates grid
class Grid:
    def __init__(self, width, height, numColumns, numRows):
        self.columnPoints = []
        self.rowPoints = []
        self.points = [self.columnPoints, self.rowPoints]

        for i in range(numColumns):
            self.columnPoints.append(int((width / numColumns) * (i + 1)))

        for i in range(numRows):
            self.rowPoints.append(int((height / numRows) * (i + 1)))

    def drawGrid(self, window_surface):
        self.totalPoints = len(self.columnPoints) * len(self.rowPoints)

        for i in range(len(self.columnPoints)):
            for k in range(len(self.rowPoints)):
                pygame.draw.rect(window_surface, '#000000', (self.points[0][i], self.points[1][k], 4, 4), 0)

    def getRows(self):
        return self.rowPoints

    def getColumns(self):
        return self.columnPoints

    def getPoints(self):
        return self.points