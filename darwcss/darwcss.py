from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import List, Any, Union
from inspect import currentframe
from textwrap import indent
from colorsys import rgb_to_hls, rgb_to_hsv, rgb_to_yiq


def render(obj):
    if hasattr(obj, '__render__'):
        return obj.__render__()
    elif obj is None: 
        return "none" # None requires specific serialization.
    else:
        return f"{obj}" # Serialize to string

class RenderableObject:
    def __render__(self):
        pass
    
    def __add__(self, other):
        return f"{render(self)} {render(other)}"
    
    def __radd__(self, other):
        return f"{render(other)} {render(self)}"
        
@dataclass
class ColorValue(RenderableObject):
    red: int
    green: int
    blue: int
    typ: str = "rgb"
    
    def __render__(self):
        return f"rgb({self.red}, {self.green}, {self.blue})" if self.typ == "rgb" else f"#{self.red}{self.green}{self.blue}"
        
@dataclass
class NumericValue(RenderableObject):
    value: Union[float, int]
    unit: str

    def __render__(self):
        return f"{self.value}{self.unit}"
        
@dataclass
class Style:
    name: str
    value: Any
    important: bool = False

    def __post_init__(self):
        self.value = render(self.value)
        f = currentframe().f_back.f_back
        l, g = f.f_locals, f.f_globals
        if l.get("DARWCSS_AUTO", g.get("DARWCSS_AUTO", False)):
            try:
                selector_name = l.get("DARWCSS_SELECTOR", g.get("DARWCSS_SELECTOR", "selector"))
                selector = l[selector_name]
            except KeyError as exc:
                raise NameError(f"Selector can not found in local namespace.") from exc
            else:
                selector.append(self)

@dataclass
class Selector:
    area: str
    styles: List[Style] = field(default_factory=list)
    
    def __add__(self, other):
        self.styles.append(other)
        
    def __iadd__(self, other):
        self + other
        return self
    
    def append(self, other):
        self.styles.append(other)

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
            yield selector
        finally:
            self.selectors.append(selector)
            
    __call__ = render
