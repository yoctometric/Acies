import pygame
import pygame_gui
from toolbar import Toolbar
from grid import Grid
import tool

SCREEN_DIMENSIONS = (1024, 600)

pygame.init()

pygame.display.set_caption('Acies')
window_surface = pygame.display.set_mode(SCREEN_DIMENSIONS)

background = pygame.Surface(SCREEN_DIMENSIONS)
background.fill(pygame.Color('#FFFFFF'))

# set ui manager and theme file
ui_manager = pygame_gui.UIManager(SCREEN_DIMENSIONS, "theme.json")


<<<<<<< HEAD
# initialize the toolbar and grid
toolbarHeight = 60
numColumns = 60
numRows = int((1 - (toolbarHeight-50)/SCREEN_DIMENSIONS[1]) * numColumns) # makes the grid dots square, given toolbar height and number columns
grid = Grid(SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1]-toolbarHeight, numColumns, numRows)
tb = Toolbar(ui_manager, toolbarHeight, SCREEN_DIMENSIONS)

# initialize tool to LineDrawer
selected_tool = tool.LineDrawer()
=======
# initialize the toolbar
tb = Toolbar(ui_manager, 100, SCREEN_DIMENSIONS)
grid = Grid(SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1], 16, 9)
>>>>>>> 93d0e4c492e32ead22bdc6bc5a803f9bb46dea66

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0 # time since last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        elif event.type == pygame.MOUSEMOTION:
            selected_tool.move_to(pygame.mouse.get_pos())
        
        ui_manager.process_events(event)

    ui_manager.update(time_delta)

    window_surface.blit(background, (0, 0))

    # draw objects
    grid.drawGrid(window_surface)
    selected_tool.drawTool(window_surface)

    # since UI is top level, drawn last
    ui_manager.draw_ui(window_surface)

    pygame.display.update()