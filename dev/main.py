import pygame
import pygame_gui
from toolbar import Toolbar, ERASE_ID, DRAW_LINE_ID, DRAW_ORB_ID, EDIT_ID, DUPLICATE_ID, EYE_DROPPER_ID, CLEAR_BOARD_ID, EXPORT_BOARD_ID
from sidebar import Sidebar, LINEEDIT_VOLUME_SLIDER_ID, LINEEDIT_PITCH_SLIDER_ID, LINEEDIT_QUALITY_SLIDER_ID
from grid import Grid
import tool
from line import LineManager

SCREEN_DIMENSIONS = (1024, 600)

pygame.init()

pygame.display.set_caption('Acies')
window_surface = pygame.display.set_mode(SCREEN_DIMENSIONS)

background = pygame.Surface(SCREEN_DIMENSIONS)
background.fill(pygame.Color('#FFFFFF'))

# set ui manager and theme file
ui_manager = pygame_gui.UIManager(SCREEN_DIMENSIONS, "theme.json")


toolbarHeight = 60
sideBarWidth = 200

grid = Grid(20, 4, (-5, -5), SCREEN_DIMENSIONS)
lineManager = LineManager(SCREEN_DIMENSIONS)
toolbar = Toolbar(ui_manager, toolbarHeight, SCREEN_DIMENSIONS)
sidebar = Sidebar(ui_manager, sideBarWidth, toolbarHeight, SCREEN_DIMENSIONS)

# initialize tool to LineDrawer
selected_tool = tool.LineDrawer(lineManager, sidebar)

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
                selected_tool.clickAction(lineManager, toolbar, sidebar)

        # handle mouse movement
        elif event.type == pygame.MOUSEMOTION:
            selected_tool.move_to(grid.getNearestPosition(pygame.mouse.get_pos()))

            # panning: if right click held,
            if pygame.mouse.get_pressed()[2]:
                grid.panGrid(event.rel) # pan the grid
            # if not panning, call hover tool action
            else:
                selected_tool.hoverAction(lineManager)

        
        # handle toolbar button events
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            button_id = event.ui_object_id # gets parent.element, so test by 'in' not '=='
            if DRAW_LINE_ID in button_id:
                selected_tool = tool.LineDrawer(lineManager, sidebar)
            elif DRAW_ORB_ID in button_id:
                selected_tool = tool.OrbDrawer(lineManager, sidebar)
            elif EDIT_ID in button_id:
                selected_tool = tool.Edit(lineManager, sidebar)
            elif ERASE_ID in button_id:
                selected_tool = tool.Eraser(lineManager, sidebar)
            elif DUPLICATE_ID in button_id:
                selected_tool = tool.Duplicator(lineManager, sidebar)
            elif EYE_DROPPER_ID in button_id:
                selected_tool = tool.EyeDropper(lineManager, sidebar)
            elif CLEAR_BOARD_ID in button_id:
                print("not really a tool.")
            elif EXPORT_BOARD_ID in button_id:
                print("Exported Board!")
                selected_tool = tool.ExportBoard(lineManager, sidebar)

        # handle sidebar orb/line edit events
        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            slider_id = event.ui_object_id
            if LINEEDIT_VOLUME_SLIDER_ID in slider_id:
                sidebar.editSelectedLine(parameter="volume", value=event.value)
            elif LINEEDIT_PITCH_SLIDER_ID in slider_id:
                sidebar.editSelectedLine(parameter="pitch", value=event.value)
            elif LINEEDIT_QUALITY_SLIDER_ID in slider_id:
                sidebar.editSelectedLine(parameter="quality", value=event.value)

        ui_manager.process_events(event)

    ui_manager.update(time_delta)

    window_surface.blit(background, (0, 0))

    # draw objects
    grid.drawGrid(window_surface)
    lineManager.renderLines(window_surface, grid.getGridOffset())
    selected_tool.drawTool(window_surface)

    # since UI is top level, drawn last
    ui_manager.draw_ui(window_surface)

    pygame.display.update()