
import pygame
import pygame_gui

# defines the toolbar ui layout
class Toolbar:
    """
    The Toolbar class defines the UI layout for the toolbar at the bottom of the screen.

    Init:
        manager: the pygame_gui.UIManager to render to
        height (int): the height in pixels for the toolbar to take up
        screen_dimensions (tuple): the dimensions of the screen for the toolbar to expand into
    
    """
    def __init__(self, manager, height, screen_dimensions) -> None:
        self.panel_rect = pygame.Rect(0, screen_dimensions[1] - height, screen_dimensions[0], height)

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
        button_x = button_x_spacing # initialize the x position of the current button to the button spacing

        # line drawer
        self.draw_line_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, button_y), button_size),
            text="",
            tool_tip_text='draw line',
            manager=manager,
            container = self.panel
        )

        # move position for next button
        button_x += button_size[0] + button_x_spacing
        # line eraser
        self.erase_line_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, button_y), button_size),
            text="",
            tool_tip_text='erase line',
            manager=manager,
            container = self.panel
        )

        # move position for next button
        button_x += button_size[0] + button_x_spacing
        # orb drawer
        self.draw_orb_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, button_y), button_size),
            text="",
            tool_tip_text ='draw orb',
            manager=manager,
            container = self.panel
        )

        # move position for next button
        button_x += button_size[0] + button_x_spacing
        # orb eraser
        self.erase_orb_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, button_y), button_size),
            text="",
            tool_tip_text='erase orb',
            manager=manager,
            container = self.panel
        )

        # move position for next button
        button_x += button_size[0] + button_x_spacing
        # duplicator
        self.duplicate_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, button_y), button_size),
            text="",
            tool_tip_text='duplicate',
            manager=manager,
            container = self.panel
        )

        # now load and attach images to their buttons

        
