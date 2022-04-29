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


class TestLineManager(unittest.TestCase):
    
    def setUp(self):
        # Overview---
            # add the start of a line
            # add a new point on the line
            # add a new point on the line
            # add a new point on the start of the line, concluding the line

            # FAIL add the start of a new line at a point along an existing line 
        
            # FAIL add the start of a new line at the start of an existing line
            
            # add the start of a new line
            # FAIL add a new point on the line that crosses the first line
    
        self.testLineManager = LineManager((100,100))

    def test_addLine(self):
        # Testing Invalid Inputs:
        # with self.assertRaises(TypeError):
        #     self.testListNone[:1]
        # print(self.testLineManager.addLine((2,3,4)))
        self.assertRaises(ValueError, self.testLineManager.addLine((2,3,4)))
        # self.testLineManager.addLine((2,10))
        # self.assertself.testLineManager.addLine(())

    def test_overlapping(self):
        pass

    def test_completeLine(self):
        pass

    def test_getLineAt(self):
        pass

    def test_getLineAtOrOver(self):
        pass




    # IMPORTANT: The function crosses() is IN-PROGRESS so it is currently nonfunctional.
    # This test is for when crosses() is debugged and fixed, to see if it works then.
    def test_crosses(self):
        # # Valid Test(s):
        # self.assertTrue(self.testLineManager.crosses((5,15),(7,5))
        # # Invalid Test(s):
        # self.assertFalse(x)
        pass


if __name__ == '__main__':
    unittest.main()