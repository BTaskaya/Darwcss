import unittest
from darwcss.darwcss import ColorValue, render

class TestColorValue(unittest.TestCase):
    def test_output_rgb(self):
        red = ColorValue(255, 0, 0)
        blue = ColorValue(0, 0, 255, "rgb")
        
        self.assertEqual(render(red), "rgb(255, 0, 0)")
        self.assertEqual(render(blue), "rgb(0, 0, 255)")
        
    def test_output_hex(self):
        purple = ColorValue("fa", "ff", "ca", "hex")
        self.assertEqual(render(purple), "#faffca")
        
if __name__ == '__main__':
    unittest.main()
