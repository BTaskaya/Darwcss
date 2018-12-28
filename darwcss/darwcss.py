from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import List, Any, Union
from inspect import currentframe
from textwrap import indent
from colorsys import rgb_to_hls, rgb_to_hsv, rgb_to_yiq

class AutoAddSelectorNotFoundInScope(Exception):
    pass

@dataclass
class ColorValue:
    red: int
    green: int
    blue: int
    typ: str = "rgb"

@dataclass
class NumericValue:
    value: Union[float, int]
    unit: str
    
@dataclass
class Style:
    name: str
    value: Any
    important: bool = False

    def __post_init__(self):
        self.value = CSS.cast(self.value)
        f = currentframe().f_back.f_back.f_globals
        if f.get("DARWCSS_AUTO", False):
            try:
                f[f.get("DARWCSS_SELECTOR", 'selector')].append(self)
            except KeyError as exc:
                raise AutoAddSelectorNotFoundInScope from exc

@dataclass
class Selector:
    area: str
    styles: List[Style] = field(default_factory=list)


class CSS:
    def __init__(self, conf=None):
        self.selectors = []
        self.conf = conf or {}
        
    def render(self):
        css = ""
        for selector in self.selectors:
            rules = ""
            for style in selector.styles:
                rules += f"{style.name}: {style.value}{' !important' if style.important else ''};\n"
            css += f"{selector.area}{'{'}\n{indent(rules, ' '*self.conf.get('indent', 4))}{'}'}\n"
        return css

    @contextmanager
    def selector(self, area):
        selector = Selector(area)
        try:
            yield selector.styles
        finally:
            self.selectors.append(selector)

    @staticmethod
    def cast(value):
        if isinstance(value, str):
            return value
        
        elif isinstance(value, float) or isinstance(value, int):
            return f"{value}" # casts value to string with fstring's performance instead of str() call
        
        elif isinstance(value, NumericValue):
            return f"{value.value}{value.unit}"
            
        elif isinstance(value, ColorValue):
            if value.typ == "rgb":
                return f"rgb({value.red}, {value.green}, {value.blue})"
            elif value.typ == "hsl":
                return f"hsl({value.red}, {value.green}%, {value.blue}%)"
            elif value.typ == "hex":
                return f"#{value.red}{value.green}{value.blue}"
            else:
                return "black"
        else:
            return "none"
            
    __call__ = render
