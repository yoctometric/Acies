import pygame
import pygame_gui
from line import Line, Orb

SIDEBAR_PANEL_ID = "#sidebar_panel"
SIDEBAR_TITLE_ID = "#sidebar_title"
SIDEBAR_ORBEDIT_PANEL_ID = "#sidebar_orbedit_panel"
SIDEBAR_LINEEDIT_PANEL_ID = "#sidebar_lineedit_panel"
LINEEDIT_VOLUME_SLIDER_ID = "#lineedit_volume_slider"
LINEEDIT_PITCH_SLIDER_ID = "#lineedit_pitch_slider"
LINEEDIT_QUALITY_SLIDER_ID = "#lineedit_quality_slider"

# defines the sidebar layout and handles appearing/disappearing
class Sidebar:
    def __init__(self, manager, width: float, bottomMargin: float, screenDimensions: tuple) -> None:
        self.screenDimensions = screenDimensions
        self.width = width
        self.bottomMargin = bottomMargin
        self.panelRect = pygame.Rect(screenDimensions[0] - width, 0, screenDimensions[0], screenDimensions[1] - bottomMargin)

        # set by sidebar when editing
        self.selectedOrb = None
        self.selectedLine = None

        # this statement defines and passes the panel to the ui manager
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=self.panelRect, 
            manager=manager, starting_layer_height=1,
            object_id=SIDEBAR_PANEL_ID
        )


        # add title
        self.title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0, 0, width, 50),
            manager=manager, text="Edit element",
            object_id=SIDEBAR_TITLE_ID, 
            container=self.panel,
            anchors = {'top': 'top',
                        'bottom': 'top',
                        'left': 'left',
                        'right': 'left'}
        )


        # orb edit sub-panel. allows setting visibility of the all orb edit elements in one call
        # the "-2" magic number is 2x the theme file's panel theme border width parameter and allows the true centering of the panel.
        self.orbEditPanel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(-2, 50, width, self.panelRect.height - 50),
            manager=manager, starting_layer_height=1,
            object_id=SIDEBAR_ORBEDIT_PANEL_ID,
            container=self.panel,
            margins={"top": 0, "left": 0, "right": 0, "bottom": 0},
            anchors= {'top': 'top',
                        'bottom': 'top',
                        'left': 'left',
                        'right': 'left'}
        )
    
        # edit orb speed label
        self.orbSpeedLabel = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0, 35, width, 20),
            manager=manager, text="Edit Orb Speed",
            container=self.orbEditPanel
        )

        # slider for orb speed editing
        self.orbSpeedSlider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(15, 60, width-30, 15),
            start_value=1,
            value_range=[1,5],
            manager=manager,
            container=self.orbEditPanel
        )

        # line edit sub-panel
        self.lineEditPanel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(-2, 50, width, self.panelRect.height - 50),
            manager=manager, starting_layer_height=1,
            object_id=SIDEBAR_LINEEDIT_PANEL_ID,
            container=self.panel,
            margins={"top": 0, "left": 0, "right": 0, "bottom": 0},
            anchors= {'top': 'top',
                        'bottom': 'top',
                        'left': 'left',
                        'right': 'left'}
        )

        # line edit volume text
        self.orbSpeedLabel = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0, 35, width, 20),
            manager=manager, text="Edit Line Volume",
            container=self.lineEditPanel
        )

        # slider for line volume editing
        self.orbSpeedSlider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(15, 60, width-30, 15),
            start_value=50,
            value_range=[0,100],
            manager=manager,
            object_id=LINEEDIT_VOLUME_SLIDER_ID,
            container=self.lineEditPanel
        )

        # line edit pitch text
        self.orbSpeedLabel = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0, 95, width, 20),
            manager=manager, text="Edit Line Pitch",
            container=self.lineEditPanel
        )

        # slider for line pitch editing
        self.orbSpeedSlider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(15, 120, width-30, 15),
            start_value=50,
            value_range=[0,100],
            manager=manager,
            object_id=LINEEDIT_PITCH_SLIDER_ID,
            container=self.lineEditPanel
        )

        # line edit quality text
        self.orbSpeedLabel = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0, 155, width, 20),
            manager=manager, text="Edit Line Quality",
            container=self.lineEditPanel
        )

        # slider for line quality editing
        self.orbSpeedSlider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(15, 180, width-30, 15),
            start_value=50,
            value_range=[0,100],
            manager=manager,
            object_id=LINEEDIT_QUALITY_SLIDER_ID,
            container=self.lineEditPanel
        )

        self.setPanelSide(2) # move panel off screen


    # shows edit panel for an orb
    def showOrbEdit(self, orb: Orb, side: int):
        self.orbEditPanel.show()
        self.lineEditPanel.hide()
        self.setPanelSide(side)
        self.selectedOrb = orb


    # shows edit panel for a line
    def showLineEdit(self, line: Line, side: int):
        self.orbEditPanel.hide()
        self.lineEditPanel.show()
        self.setPanelSide(side)
        self.selectedLine = line


    # set the side the panel is appearing on. 0: left, 1: right, 2+: off screen (hidden)
    def setPanelSide(self, side: int=1):

        x = (self.screenDimensions[0] - self.width) * side
        self.panel.set_position((x, 0))
        self.panel.set_dimensions((self.width, self.screenDimensions[1] - self.bottomMargin))

        if side > 1:
            # offscreen, deselect selection
            self.selectedLine = None
            self.selectedOrb = None

    
    # called by main to handle slider events and edit the selected line
    def editSelectedLine(self, parameter: str, value: float):
        if parameter == "volume":
            self.selectedLine.setVolume(value)
        elif parameter == "pitch":
            self.selectedLine.setPitch(value)
        elif parameter == "quality":
            self.selectedLine.setQuality(value)
