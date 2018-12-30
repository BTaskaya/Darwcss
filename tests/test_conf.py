import unittest
from darwcss.darwcss import CSS, Selector, Style


class TestConf(unittest.TestCase):
    rendered_css = ".home{\n    a: b;\n    c: d;\n}\n"

    def test_conf_inheritance_selector(self):
        css = CSS({"darwcss_auto": True})
        
        with css.selector('.home') as selector:
            selector += Style("a", "b")
            selector += Style("c", "d")
        
        self.assertEqual(css.render(), self.rendered_css)

if __name__ == "__main__":
    unittest.main()
