import unittest
from line import Line, LineManager, Point, Orb

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



if __name__ == '__main__':
    unittest.main()