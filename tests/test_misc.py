import unittest
from darwcss.darwcss import *


class TestMisc(unittest.TestCase):
    def test_multiple_value_types(self):
        border_size = NumericValue(5, "px")
        border_type = "solid"
        border_color = ColorValue(255, 0, 0)

        border_style = Style("border", border_size + border_type + border_color)
        self.assertEqual(border_style.value, "5px solid rgb(255, 0, 0)")


if __name__ == "__main__":
    unittest.main()
