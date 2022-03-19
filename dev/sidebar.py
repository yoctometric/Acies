import pygame
import pygame_gui
from line import Line, Orb

SIDEBAR_PANEL_ID = "#sidebar_panel"
SIDEBAR_TITLE_ID = "#sidebar_title"

# defines the sidebar layout and handles appearing/disappearing
class Sidebar:
    def __init__(self, manager, width: float, bottomMargin: float, screenDimensions: tuple) -> None:
        self.screenDimensions = screenDimensions
        self.width = width
        self.bottomMargin = bottomMargin
        self.panelRect = pygame.Rect(screenDimensions[0] - width, 0, screenDimensions[0], screenDimensions[1] - bottomMargin)

        # this statement defines and passes the panel to the ui manager
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=self.panelRect, 
            manager=manager, starting_layer_height=1,
            object_id=SIDEBAR_PANEL_ID
        )


        # add title
        self.title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.panelRect.x, 0, width, 50),
            manager=manager, text="Edit Line",
            object_id=SIDEBAR_TITLE_ID
        )
    
        self.setPanelSide(2) # move panel off screen


    # shows edit panel for an orb
    def showOrbEdit(self, orb: Orb, side: int):

        self.setPanelSide(side)


    # shows edit panel for a line
    def showLineEdit(self, line: Line, side: int):

        self.setPanelSide(side)


    # set the side the panel is appearing on. 0: left, 1: right, 2+: off screen (hidden)
    def setPanelSide(self, side: int=1):
        # TODO: also adjust the children. how? containers / anchors are poorly documented and confusing

        x = (self.screenDimensions[0] - self.width) * side
        self.panel.set_position((x, 0))
        self.panel.set_dimensions((self.width, self.screenDimensions[1] - self.bottomMargin))

