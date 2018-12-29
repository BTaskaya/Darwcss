import unittest
from darwcss.darwcss import CSS, Style


class TestCSS(unittest.TestCase):
    rendered_css = ".home{\n    a: b;\n    c: d;\n}\n"

    def test_css_with(self):
        css = CSS()
        with css.selector(".home") as selector:
            selector.append(Style("a", "b"))
            selector.append(Style("c", "d"))

        self.assertEqual(css.render(), self.rendered_css)

    def test_css_with_iadd(self):
        css = CSS()
        with css.selector(".home") as selector:
            selector += Style("a", "b")
            selector += Style("c", "d")

        self.assertEqual(css.render(), self.rendered_css)

    def test_css_auto_add(self):
        css = CSS()
        DARWCSS_AUTO = True

        with css.selector(".home") as selector:
            Style("a", "b")
            Style("c", "d")

        self.assertEqual(css.render(), self.rendered_css)

    def test_css_auto_add_different_selector(self):
        css = CSS()
        DARWCSS_AUTO = True
        DARWCSS_SELECTOR = "test"

        with css.selector(".home") as test:
            Style("a", "b")
            Style("c", "d")

        self.assertEqual(css.render(), self.rendered_css)

    def test_css_auto_add_different_selector_name_error(self):
        css = CSS()
        DARWCSS_AUTO = True
        DARWCSS_SELECTOR = "test"

        with css.selector(".home") as selector:
            with self.assertRaises(NameError):
                Style("a", "b")


if __name__ == "__main__":
    unittest.main()
