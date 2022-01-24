import unittest
import grid
import os

class EmptyTest(unittest.TestCase):
    """
    test of grid.Grid class with an empty instance
    """
    def setUp(self):
        self.g = grid.Grid()

    def test_empty_instance(self):
        """
        Create a Grid object from ETOPO1 data
        Test all state variables
        """
        self.assertIsNone(self.g.grdfile)
        self.assertIsNone(self.g.maskfile)
        self.assertEqual(self.g.operations, [])

    def test_subset(self):
        """
        Create a subset of the data without
        an empty grid class
        """
        region=('-98','-80','18','30')
        dg = self.g.subset(region)
        self.assertIsNone(dg)

    def test_load(self):
        """
        load the default global dataset
        """
        self.g.load()
        self.assertEqual(self.g.grdfile, 'data/etopo1/ETOPO1_Ice_g_gmt4.grd')

    def test_landmask(self):
        """
        create a landmask from the global dataset
        """
        self.g.create_landmask()

    def tearDown(self):
        del self.g

class LoadTest(unittest.TestCase):
    """
    test of grid.Grid with a default grid
    """
    def setUp(self):
        self.g = grid.Grid()
        self.g.load()

    def test_subset(self):
        """
        Create a subset of the data without
        an empty grid class. See if the data file is
        created

        'ETOPO1_Ice_g_gmt4_sub.grd'
        """
        region=('-98','-80','18','30')
        dg = self.g.subset(region)
        self.assertIsInstance(dg, grid.DerivedGrid)
        expected_file = 'ETOPO1_Ice_g_gmt4_sub.grd'
        output_file = os.path.exists(expected_file)
        self.assertTrue(output_file)
        self.assertEqual(self.g.operations, dg.operations)
        os.remove(expected_file)

    def test_landmask(self):
        """
        Create a landmask of the data without
        an empty grid class. See if the data file is
        created

        'ETOPO1_Ice_g_gmt4_lm.grd'
        """
        dg = self.g.create_landmask()
        self.assertIsInstance(dg, grid.DerivedGrid)
        expected_file = 'ETOPO1_Ice_g_gmt4_lm.grd'
        output_file = os.path.exists(expected_file)
        self.assertTrue(output_file)
        os.remove(expected_file)

    def tearDown(self):
        del self.g

if __name__ == '__main__':
    unittest.main()
