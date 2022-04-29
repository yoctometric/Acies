import unittest
from line import Line, LineManager, Point, Orb
from grid import Grid

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


if __name__ == '__main__':
    unittest.main()