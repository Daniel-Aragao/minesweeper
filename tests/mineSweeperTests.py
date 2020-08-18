import unittest
from .context import minesweeper
from minesweeper.core.MineSweeper import MineSweeper

class MineSweeperTests(unittest.TestCase):
    
    def test_dimensions(self):
        ms = MineSweeper(8, 16)
        self.assertEqual((8, 16), ms.get_dimensions())

    def test_bombs_amount(self):
        x = 0.25
        ms = MineSweeper(8, 16, percent_of_tiles_as_bombs=x)
        self.assertEqual(int(8*16*x), ms.get_bombs_quantity())

if __name__ == '__main__':
    unittest.main()