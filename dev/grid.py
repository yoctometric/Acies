import pygame
import pygame_gui

SCREEN_DIMENSIONS = (800, 600)

pygame.init()

pygame.display.set_caption('Grid Alpha Build')
window_surface = pygame.display.set_mode(SCREEN_DIMENSIONS)

background = pygame.Surface(SCREEN_DIMENSIONS)
background.fill(pygame.Color('#FFFFFF'))

# set 
ui_manager = pygame_gui.UIManager(SCREEN_DIMENSIONS, "theme.json")

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

    def drawGrid(self):
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


#Initialize grid
grid = Grid(SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1], 5, 5)

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0 # time since last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        
        ui_manager.process_events(event)

    ui_manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    ui_manager.draw_ui(window_surface)
    grid.drawGrid()

    pygame.display.update()