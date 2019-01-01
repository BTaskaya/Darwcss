import unittest
from darwcss.darwcss import CSS, Selector, Style


class TestConf(unittest.TestCase):
    def test_conf_inheritance_selector(self):
        css = CSS({"darwcss_auto": True})
        
        with css.selector('.home') as selector:
            self.assertEqual(selector.meta_cfg, {"darwcss_auto": True})

if __name__ == "__main__":
    unittest.main()
