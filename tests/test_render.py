import unittest
from darwcss.darwcss import render

class TestRender(unittest.TestCase):
    def test_render_string(self):
        self.assertEqual(render("merhaba"), "merhaba")
        self.assertEqual(render("T3est"), "T3est")
    
    def test_render_none(self):
        self.assertEqual(render(None), "none")
    
    def test_render_renderable(self):
        class RenderableObject:
            def __render__(self) -> str:
                return "ABC"
            
        self.assertEqual(render(RenderableObject()), "ABC")

    def test_render_string_converter(self):
        self.assertEqual(render(32), "32")

if __name__ == '__main__':
    unittest.main()
