
import pygame
import pygame_gui


SCREEN_DIMENSIONS = (800, 600)

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode(SCREEN_DIMENSIONS)

background = pygame.Surface(SCREEN_DIMENSIONS)
background.fill(pygame.Color('#FFFFFF'))

# set 
ui_manager = pygame_gui.UIManager(SCREEN_DIMENSIONS, "theme.json")


hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                             text='Say Hello',
                                             manager=ui_manager)


# defines the toolbar ui layout
class Toolbar:
    def __init__(self, manager, height) -> None:
        self.panel_rect = pygame.Rect(0, SCREEN_DIMENSIONS[1] - height, SCREEN_DIMENSIONS[0], height)

        # this statement defines and passes the panel to the ui manager
        self.panel = pygame_gui.elements.UIPanel(
                    relative_rect=self.panel_rect, 
                    manager=manager, starting_layer_height=1
        )

        # now create each of the buttons for the tools

        button_scale = 0.75
        button_size = (height * button_scale, height * button_scale)
        button_y = (height - (height * button_scale)) / 2
        button_x_spacing = 10

        # pen
        self.pen_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((button_size[0] + button_x_spacing) * 1, button_y), button_size),
            text='pen',
            manager=ui_manager,
            container = self.panel
        )

        # eraser
        self.pen_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((button_size[0] + button_x_spacing) * 2, button_y), button_size),
            text='eraser',
            manager=ui_manager,
            container = self.panel
        )

# initialize the toolbar
toolbar = Toolbar(ui_manager, 100)


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

    pygame.display.update()