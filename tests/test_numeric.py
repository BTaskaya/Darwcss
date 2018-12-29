import unittest
from darwcss.darwcss import NumericValue, render

class TestNumericValue(unittest.TestCase):
    def test_numeric_render(self):
        t = NumericValue(5, "px")
        self.assertEqual(render(t), "5px")
        
        x = NumericValue(30, "%")
        self.assertEqual(render(x), "30%")

if __name__ == '__main__':
    unittest.main()
