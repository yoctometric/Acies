import pygame
import pygame_gui
from toolbar import Toolbar, ERASE_ID, DRAW_LINE_ID, DRAW_ORB_ID, DUPLICATE_ID, EYE_DROPPER_ID, CLEAR_BOARD_ID
from grid import Grid, ResizableGrid
import tool

SCREEN_DIMENSIONS = (1024, 600)

pygame.init()

pygame.display.set_caption('Acies')
window_surface = pygame.display.set_mode(SCREEN_DIMENSIONS)

background = pygame.Surface(SCREEN_DIMENSIONS)
background.fill(pygame.Color('#FFFFFF'))

# set ui manager and theme file
ui_manager = pygame_gui.UIManager(SCREEN_DIMENSIONS, "theme.json")


# initialize the toolbar and grid
toolbarHeight = 60
numColumns = 60
# numRows = int((1 - (toolbarHeight-50)/SCREEN_DIMENSIONS[1]) * numColumns) # makes the grid dots square, given toolbar height and number columns
# grid = Grid(SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1]-toolbarHeight, numColumns, numRows)
grid = ResizableGrid(20, 4, (-5, -5), SCREEN_DIMENSIONS)

tb = Toolbar(ui_manager, toolbarHeight, SCREEN_DIMENSIONS)

# initialize tool to LineDrawer
selected_tool = tool.LineDrawer()

clock = pygame.time.Clock()
is_running = True


while is_running:
    time_delta = clock.tick(60)/1000.0 # time since last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # handle tool actions. TODO: halt tool usage while over UI
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                selected_tool.clickAction(None)

        # handle mouse movement
        elif event.type == pygame.MOUSEMOTION:
            selected_tool.move_to(grid.getNearestPosition(pygame.mouse.get_pos()))

            # panning: if right click held,
            if pygame.mouse.get_pressed()[2]:
                grid.panGrid(event.rel) # pan the grid

        
        # handle toolbar button events
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            button_id = event.ui_object_id # gets parent.element, so test by 'in' not '=='
            if DRAW_LINE_ID in button_id:
                selected_tool = tool.LineDrawer()
            elif DRAW_ORB_ID in button_id:
                selected_tool = tool.OrbDrawer()
            elif ERASE_ID in button_id:
                selected_tool = tool.Eraser()
            elif DUPLICATE_ID in button_id:
                selected_tool = tool.Duplicator()
            elif EYE_DROPPER_ID in button_id:
                selected_tool = tool.EyeDropper()
            elif CLEAR_BOARD_ID in button_id:
                print("not really a tool.")
            
        ui_manager.process_events(event)

    ui_manager.update(time_delta)

    window_surface.blit(background, (0, 0))

    # draw objects
    grid.drawGrid(window_surface)
    selected_tool.drawTool(window_surface)

    # since UI is top level, drawn last
    ui_manager.draw_ui(window_surface)

    pygame.display.update()