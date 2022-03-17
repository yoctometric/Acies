import pygame
import pygame_gui


# button id defines. per pygame_gui standards, start with '#' and follow snake_case
DRAW_LINE_ID = "#draw_line_button"
DRAW_ORB_ID = "#draw_orb_button"
ERASE_ID = "#erase_button"
DUPLICATE_ID = "#duplicate_line_button"
EYE_DROPPER_ID = "#eye_dropper_button"
CLEAR_BOARD_ID = "#clear_board_button"


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

        # line drawer (pencil)
        self.draw_line_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, button_y), button_size),
            text="",
            tool_tip_text='draw line',
            manager=manager,
            container = self.panel,
            object_id=DRAW_LINE_ID
        )

        # move position for next button
        button_x += button_size[0] + button_x_spacing
        # orb drawer
        self.draw_orb_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, button_y), button_size),
            text="",
            tool_tip_text ='draw orb',
            manager=manager,
            container=self.panel,
            object_id=DRAW_ORB_ID
        )

        # move position for next button
        button_x += button_size[0] + button_x_spacing
        # general eraser
        self.erase_orb_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, button_y), button_size),
            text="",
            tool_tip_text='erase',
            manager=manager,
            container=self.panel,
            object_id=ERASE_ID
        )

        # move position for next button
        button_x += button_size[0] + button_x_spacing
        # duplicator
        self.duplicate_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, button_y), button_size),
            text="",
            tool_tip_text='duplicate',
            manager=manager,
            container=self.panel,
            object_id=DUPLICATE_ID
        )

        # move position for next button
        button_x += button_size[0] + button_x_spacing
        # eye dropper
        self.eye_dropper_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, button_y), button_size),
            text="",
            tool_tip_text='eye dropper',
            manager=manager,
            container=self.panel,
            object_id=EYE_DROPPER_ID
        )

        # move position for next button
        button_x += button_size[0] + button_x_spacing
        # clear board (trash can) TODO: should this be aligned right so that it isnt so close to the other buttons?
        self.clear_board_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, button_y), button_size),
            text="",
            tool_tip_text='clear board. is this even a tool? maybe should align right and make it a click, confirm popup sorta thing',
            manager=manager,
            container=self.panel,
            object_id=CLEAR_BOARD_ID
        )

        # now load and attach images to their buttons

        
