from re import X
import pygame
# This file contains all of the classes relating to Tools and placement
# so, the toolbar will recieve a click and say "selected_tool = LineDrawer()" for example

# the parent class of all tools. main makes it follow the mouse
class Tool():
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.cursor_image = None # child instance sets after super init
        self.cursor_rect = None


    # called my main to update tool position
    def move_to(self, pos: tuple):
        self.x = pos[0]
        self.y = pos[1]


    # called by main to draw the cursor image of the tool
    def drawTool(self, window_surface: pygame.Surface):
        # align rect so that the bottom left corner of the image is at the cursor
        r = self.cursor_rect
        r.x = self.x - r.width
        r.y = self.y - r.height
        window_surface.blit(self.cursor_image, r)
    

    # called by child to load up and set the cursor image of the tool
    def setCursorImage(self, filePath: str):
        self.cursor_image = pygame.image.load(filePath).convert()
        self.cursor_rect = self.cursor_image.get_rect()


# contains functionality for drawing lines
class LineDrawer(Tool):
    def __init__(self) -> None:
        super().__init__()

        # load image for LineDrawer
        super().setCursorImage("resources/line_drawer_cursor.png")