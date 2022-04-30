from tkinter.filedialog import test
import unittest
from line import Line, LineManager, Point, Orb
from tool import Tool
from sidebar import Sidebar
from pygame_gui import UIManager
from toolbar import Toolbar
from grid import Grid
import pygame
import pygame_gui


class TestLine(unittest.TestCase):
    
    def setUp(self) -> None:
        self.line = Line((0, 0), (0, 0))

        return super().setUp()

    # testing for add point. Added point is only sustained for duration of this method
    def testAddPoint(self):
        # Valid
        self.line.addPoint((1, 1))
        self.assertEqual(len(self.line.getPath()), 2, "add point failed to add a new point")

        # Invalid
        self.assertRaises(AssertionError, self.line.addPoint, 1)
    
    # testing for add point from worldspace. Initial len is still 1 because testAddPoint does not affect self.line permanently
    def testAddPointFromWorldspace(self):
        # Valid
        self.line.addPointFromWorldspace((50, 50), (10, 10))
        self.assertEqual(len(self.line.getPath()), 2, "add point from worldspace failed to add a new point")
        self.assertEqual(self.line.getPath()[1].position, (40, 40), "worldspace to linespace conversion failed")

        # Invalid
        self.assertRaises(TypeError, self.line.addPointFromWorldspace, 1, 1)
    
    # adds a point and then tests deleting it
    def testDeletePoint(self):
        # Valid
        self.line.addPointFromWorldspace((50, 50), (10, 10))
        self.assertEqual(len(self.line.getPath()), 2, "add point setup for delete point failed")

        self.line.deletePoint((50, 50), (10, 10))
        self.assertEqual(len(self.line.getPath()), 1, "failed to delete point from line")

        # Invalid
        self.assertFalse(self.line.deletePoint((50, 50), (10, 10)), "somehow managed to delete an already deleted point")

    # adds a couple points and then tests that they are retrieved correctly
    def testGetPathScreenSpace(self):
        # Valid
        self.line.addPointFromWorldspace((50, 50), (10, 10))
        self.line.addPointFromWorldspace((60, 60), (10, 10))

        path = self.line.getPathScreenSpace((5, 5))
        self.assertEqual(path[1], (45, 45), "failed to convert point to world/screen space")
        self.assertEqual(path[2], (55, 55), "failed to convert point to world/screen space")

        # Invalid
        self.assertRaises(TypeError, self.line.getPathScreenSpace, "no", "failed to raise type error")

    def tearDown(self) -> None:
        return super().tearDown()


class TestLineManager(unittest.TestCase):
    
    def setUp(self):   
        # Three different LineManagers, one for each test function 
        self.test1LineManager = LineManager((1024,600))
        self.test2LineManager = LineManager((1024,600))
        self.test3LineManager = LineManager((1024,600))

        # For completeLine() test
        self.test2LineManager.addLine((250,400))
        self.test2LineManager.addLine((350,400))
        self.test2LineManager.addLine((350,550))
        self.test2LineManager.addLine((250,550))
        self.prevLine = self.test2LineManager.lineEditing

        # For crosses() test
        self.test3LineManager.addLine((500,100))
        self.test3LineManager.addLine((800,100))
        self.test3LineManager.addLine((500,100))

    def test_addLines(self):
        # Valid:
        self.assertEqual(0,self.test1LineManager.addLine((250,400)), "Failed starting a line")
        self.assertEqual(0,self.test1LineManager.addLine((350,400)), "Failed placing a horizontal line")
        self.assertEqual(0,self.test1LineManager.addLine((350,550)), "Failed placing a vertical line")
        # Invalid:
        self.assertEqual(-1,self.test1LineManager.addLine((150,150)), "Allowed a diagonal line")

    def test_completeLine(self):
        # Valid
        self.assertEqual(0,self.test2LineManager.completeLine((250,400)), "Failed completing a valid line")
        self.test2LineManager.lineEditing = self.prevLine
        # Invalid
        self.assertEqual(-1,self.test2LineManager.completeLine((280,400)), "Allowed finishing a line to an invalid point")
    
    def test_crosses(self): # currently not working since LineManager.crosses() is in-progress
        # Invalid
        self.assertTrue(self.test3LineManager.crosses((550,50),(550,150)), "Failed to detect perpindicular crossing in middle")
        self.assertTrue(self.test3LineManager.crosses((500,50),(500,150)), "Failed to detect perpindicular crossing on left point")
        self.assertTrue(self.test3LineManager.crosses((800,50),(800,150)), "Failed to detect perpindicular crossing on right point")
        self.assertTrue(self.test3LineManager.crosses((300,100),(500,100)), "Failed to detect parallel crossing on left point")
        self.assertTrue(self.test3LineManager.crosses((800,100),(900,100)), "Failed to detect parallel crossing on right point")
        self.assertTrue(self.test3LineManager.crosses((550,100),(750,100)), "Failed to detect parallel contained within line")
        self.assertTrue(self.test3LineManager.crosses((400,100),(600,100)), "Failed to detect parallel overlapping on left")
        self.assertTrue(self.test3LineManager.crosses((600,100),(900,100)), "Failed to detect parallel overlapping on right")
        # Valid
        self.assertFalse(self.test3LineManager.crosses((400,50),(400,150)), "False pos: detected perpendicular to right of line")
        self.assertFalse(self.test3LineManager.crosses((900,50),(900,150)), "False pos: detected perpendicular to left of line")
        self.assertFalse(self.test3LineManager.crosses((450,50),(850,50)), "False pos: detected perpendicular above line")
        self.assertFalse(self.test3LineManager.crosses((550,50),(550,50)), "False pos: detected perpendicular below line")

    def test_getLineAt(self):
        # Inalid
        self.assertIsNone(self.test3LineManager.getLineAt((50,50)), "False pos: incorrectly identified point not on a line")
        # Valid
        self.assertIsNotNone(self.test3LineManager.getLineAt((500,100)), "Did not detect left edge of line")
        # getLineAt() currently is only used to detect line ends, not the middle
        self.assertIsNotNone(self.test3LineManager.getLineAt((700,100)), "Did not detect middle of line")
        self.assertIsNotNone(self.test3LineManager.getLineAt((800,100)), "Did not detect right edge of line")


class TestGrid(unittest.TestCase):

    def setUp(self) -> None:
        self.grid = Grid(20, 4, (0, 0), (1024, 600))

        return super().setUp()

    # tests panning the grid
    def testPanGrid(self):
        # Valid
        self.grid.panGrid((5, 5))
        self.assertEqual(self.grid.gridOffset, (5, 5), "Pan did not update grid offset correctly")

        # Invalid
        self.assertRaises(TypeError, self.grid.panGrid, "left", "Did not raise error on string pan")
        
    # tests rounding a position to a grid point
    def testGetNearestPosition(self):
        # Valid
        snapped = self.grid.getNearestPosition((101, 101))
        self.assertEqual(snapped, (100, 100), "did not clamp correctly")

        # Invalid
        self.assertRaises(TypeError, self.grid.getNearestPosition, 1, "did not raise type error")

    def tearDown(self) -> None:
        return super().tearDown()  


class TestTool(unittest.TestCase):
    def setUp(self) -> None:
        self.testbackground = pygame.Surface((1024,600))
        self.testwindow_surface = pygame.display.set_mode((1024,600))
        # self.testwindow_surface = self.testwindow_surface.blit(self.testbackground, (0, 0))
        self.test_ui_manager = pygame_gui.UIManager((1024,600), "theme.json")
        self.testLineManager = LineManager((1024,600))
        self.testSidebar = Sidebar(self.test_ui_manager, 200, 60, (1024,600))
        self.tool = Tool(self.testLineManager,self.testSidebar)

        return super().setUp()

    def testClickAction(self):
        #Valid
        success = self.tool.clickAction(self.testLineManager, Toolbar(self.test_ui_manager, 60, (1024,600)), self.testSidebar)
        self.assertTrue(success, "Click action failed")

        #Invalid
        self.assertRaises(TypeError, self.tool.clickAction, "testdummy", Toolbar(self.test_ui_manager, 60, (1024,600)), "Worked Unexpectedly"  ) #manager, height, screen_dimensions
        
    def testHoverAction(self):
        #Valid
        # Note: Not currently implemented. Test for future.
        success = self.tool.hoverAction(self.testLineManager)
        self.assertTrue(success, "Hover action failed")

        #Invalid
        self.assertRaises(TypeError, self.tool.clickAction, "testdummy", "Worked Unexpectedly")

    def testDrawTool(self):
        #Valid
        success = self.tool.drawTool(self.testwindow_surface)
        self.assertEqual(0, success, "Draw action failed")

        #Invalid
        self.assertRaises(TypeError, self.tool.drawTool, "testdummy", "Worked unexpectedly")

    def setCursorImage(self):
        #Valid
        success = self.tool.setCursorImage(filePath="xd")
        self.assertTrue(success, "Set Cursor Image action failed")

        #Invalid
        self.assertRaises(TypeError, self.tool.setCursorImage, 1, "Worked unexpectedly")

    def tearDown(self) -> None:
        return super().tearDown()


if __name__ == '__main__':
    unittest.main()