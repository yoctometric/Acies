
import pygame
import pygame_gui


SCREEN_DIMENSIONS = (800, 600)

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode(SCREEN_DIMENSIONS)

background = pygame.Surface(SCREEN_DIMENSIONS)
background.fill(pygame.Color('#000000'))

# set 
ui_manager = pygame_gui.UIManager(SCREEN_DIMENSIONS, "theme.json")


hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                             text='Say Hello',
                                             manager=ui_manager)


# defines the toolbar ui layout
class Toolbar:
    def __init__(self, manager: pygame_gui.UIManager, rect: pygame.Rect) -> None:
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=rect, manager=manager, starting_layer_height=1
        )


toobar = Toolbar(ui_manager, pygame.Rect(0, SCREEN_DIMENSIONS[0] - 40, SCREEN_DIMENSIONS[1], 40))



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