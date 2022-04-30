# FOR UNIT TESTS commented line 34
# This file contains all of the classes relating to Tools and placement
# so, the toolbar will recieve a click and say "selected_tool = LineDrawer()" for example

import pygame
from line import Line, LineManager, Orb
from sidebar import Sidebar
from toolbar import Toolbar
from datetime import datetime

# the parent class of all tools. main makes it follow the mouse
class Tool():
    def __init__(self, lineManager: LineManager, sidebar: Sidebar) -> None:
        self.x = 0
        self.y = 0
        self.cursor_image = None # child instance sets after super init
        self.cursor_rect = None

        # when a new tool is initialized, reset some things
        sidebar.hide()
        lineManager.lineEditing = None



    # called by main to update tool position
    def move_to(self, pos: tuple):
        self.x = pos[0]
        self.y = pos[1]

    
    # performs tool action. overridden by children. returns success or failure
    # tools should only ever need to talk to the LineManager and UI elements
    def clickAction(self, lineManager: LineManager, toolbar: Toolbar, sidebar: Sidebar) -> bool:
        if str(type(lineManager)) != "<class 'line.LineManager'>" or \
            str(type(sidebar)) != "<class 'sidebar.Sidebar'>" or \
                str(type(toolbar)) != "<class 'toolbar.Toolbar'>": 
            raise TypeError
        # print("default tool action")
        return True
    
    

    # performs tool hover function. overridden by some children (mouse motion triggers this)
    def hoverAction(self, lineManager: LineManager) -> bool:
        return True


    # called by main to draw the cursor image of the tool
    def drawTool(self, window_surface: pygame.Surface):
        # align rect so that the bottom left corner of the image is at the cursor
        r = self.cursor_rect
        if r is not None:
            r.x = self.x - r.width
            r.y = self.y - r.height
            window_surface.blit(self.cursor_image, r)
        return 0
    

    # called by child to load up and set the cursor image of the tool
    def setCursorImage(self, filePath: str):
        self.cursor_image = pygame.image.load(filePath).convert()
        self.cursor_rect = self.cursor_image.get_rect()



# contains functionality for drawing lines
class LineDrawer(Tool):
    def __init__(self, lineManager: LineManager, sidebar: Sidebar) -> None:
        super().__init__(lineManager, sidebar)

        # load image for LineDrawer
        super().setCursorImage("resources/line_drawer_cursor.png")
    
    # line click override
    def clickAction(self, lineManager: LineManager, toolbar: Toolbar, sidebar: Sidebar) -> bool:
        return lineManager.addLine((self.x, self.y))


# contains functionality for drawing orbs on lines
class OrbDrawer(Tool):
    def __init__(self, lineManager: LineManager, sidebar: Sidebar) -> None:
        super().__init__(lineManager, sidebar)

        # load image for OrbDrawer
        super().setCursorImage("resources/orb_drawer_cursor.png")

    # orb click override
    def clickAction(self, lineManager: LineManager, toolbar: Toolbar, sidebar: Sidebar) -> bool:
        l = lineManager.getLineAtOrOver((self.x, self.y))
        if l is not None:
            l.addOrb((self.x, self.y), lineManager.gridOffset)
        else:
            print("can't add orb: not over line")


# contains functionality for editing orbs and lines
class Edit(Tool):
    def __init__(self, lineManager: LineManager, sidebar: Sidebar) -> None:
        super().__init__(lineManager, sidebar)

        # load image for Edit tool
        super().setCursorImage("resources/edit_cursor.png")

    # edit click override
    def clickAction(self, lineManager: LineManager, toolbar: Toolbar, sidebar: Sidebar) -> bool:

        # get the line that the cursor is over
        targetLine = lineManager.getLineAtOrOver((self.x, self.y))

        # calc the side to show the sidebar on
        side = 1
        if self.x > (lineManager.screenDimensions[0] / 2):
            side = 0
        
        if targetLine:
            sidebar.showLineEdit(targetLine, side)

        return True


# contains fucntionality for erasing lines and orbs
class Eraser(Tool):
    def __init__(self, lineManager: LineManager, sidebar: Sidebar) -> None:
        super().__init__(lineManager, sidebar)

        # load image for Eraser
        super().setCursorImage("resources/eraser_cursor.png")  
    
    # TODO: Allow users to drag on the grid holding the eraser and delete parts of lines
    def dragAction(self, lineManager: LineManager, toolbar: Toolbar, sidebar: Sidebar) -> bool:
        # get cursor location
        # if cursor location is close to a dot (less than half the distance between dots on the grid):
        #   get line at cursor position
        #   
        pass


# contains functionality for duplicating lines and their orbs
class Duplicator(Tool):
    def __init__(self, lineManager: LineManager, sidebar: Sidebar) -> None:
        super().__init__(lineManager, sidebar)

        # load image for Duplicator
        super().setCursorImage("resources/duplicator_cursor.png")  


# contains functionality for eye dropper
class EyeDropper(Tool):
    def __init__(self, lineManager: LineManager, sidebar: Sidebar) -> None:
        super().__init__(lineManager, sidebar)

        # load image for Eye dropper
        super().setCursorImage("resources/eye_dropper_cursor.png")  


# contains functionality for export board. writes to a file with all lines, points, and orbs
class ExportBoard(Tool):
    def __init__(self, lineManager: LineManager, sidebar: Sidebar) -> None:
        super().__init__(lineManager, sidebar)
        now = datetime.now()
        dt_str = now.strftime("%d-%m-%Y_%H-%M-%S")
        f = open("ExportedBoard_" + dt_str + ".txt", "w")
        for line in lineManager.lines:
            f.write("Line: \n")
            for point in line.path:
                f.write("\tPoint: \n")
                f.write("\t\tPos: "+str(point.position[0])+", "+str(point.position[1])+"\n")
            for orb in line.orbs:
                f.write("\torb: \n")
                f.write("\t\tPos: "+str(orb.position[0])+", "+str(orb.position[1])+"\n")
                f.write("\t\tSpeed: "+str(orb.speed)+"\n")
        f.close()