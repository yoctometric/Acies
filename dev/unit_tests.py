import unittest
from line import Line, LineManager, Point, Orb
from tool import Tool
from sidebar import Sidebar
from pygame_gui import UIManager
from toolbar import Toolbar

class TestLine(unittest.TestCase):
    
    def setUp(self) -> None:
        self.line = Line((0, 0), (0, 0))

        return super().setUp()


    # testing for add point. Added point is only sustained for duration of this method
    def testAddPoint(self):
        self.line.addPoint((1, 1))
        self.assertEqual(len(self.line.getPath()), 2, "add point failed to add a new point")
    

    # testing for add point from worldspace. Initial len is still 1 because testAddPoint does not affect self.line permanently
    def testAddPointFromWorldspace(self):
        self.line.addPointFromWorldspace((50, 50), (10, 10))
        self.assertEqual(len(self.line.getPath()), 2, "add point from worldspace failed to add a new point")
        self.assertEqual(self.line.getPath()[1].position, (40, 40), "worldspace to linespace conversion failed")

    
    # adds a point and then tests deleting it
    def testDeletePoint(self):
        self.line.addPointFromWorldspace((50, 50), (10, 10))
        self.assertEqual(len(self.line.getPath()), 2, "add point setup for delete point failed")

        self.line.deletePoint((50, 50), (10, 10))
        self.assertEqual(len(self.line.getPath()), 1, "failed to delete point from line")





    def tearDown(self) -> None:
        return super().tearDown()



class testTool(unittest.TestCase):
    def setUp(self) -> None:
        self.tool = Tool(LineManager((0,0)),Sidebar(UIManager((0,0), "theme.json"),0 , 0, (0,0)))

        return super().setUp()

    def testClickAction(self):
        #Valid
        success = self.tool.clickAction(LineManager((0,0)),Sidebar(UIManager((0,0), "theme.json")), Toolbar(UIManager((0,0), 0, (0,0)), Sidebar(UIManager((0,0), 0, (0,0)), 0, 0, (0,0))))
        self.assertTrue(success, "Action failed")

        #Invalid
        self.assertRaises(TypeError, self.tool.clickAction, "testdummy", Toolbar(UIManager((0,0), 0, (0,0)), Sidebar(UIManager((0,0), 0, (0,0)), 0, 0, (0,0))), "Worked Unexpectedly"  )
        
    def testHoverAction(self):
        #Valid
        success = self.tool.hoverAction(LineManager((0,0)))
        self.assertTrue(success, "Action failed")

        #Invalid
        self.assertRaises(TypeError, self.tool.clickAction, "testdummy", "Worked Unexpectedly")

    def testDrawTool(self):
        #Valid
        success = self.tool.drawTool(window_surface)
        self.assertTrue(success, "Action failed")

        #Invalid
        self.assertRaises(TypeError, self.tool.drawTool, "testdummy", "Worked unexpectedly")

    def setCursorImage(self):
        #Valid
        success = self.tool.setCursorImage(filePath="xd")
        self.assertTrue(success, "Action failed")

        #Invalid
        self.assertRaises(TypeError, self.tool.setCursorImage, 1, "Worked unexpectedly")


    def tearDown(self) -> None:
        return super().tearDown()

if __name__ == '__main__':
    unittest.main()