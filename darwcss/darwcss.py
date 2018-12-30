from __future__ import annotations
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import List, Any, Union, Optional, Generator, Dict, Tuple
from inspect import currentframe
from textwrap import indent
from colorsys import rgb_to_hls
from enum import Enum


def clean_name(css_name: str) -> str:
    if css_name.startswith('.'):
        css_name = css_name.replace('.', 'cls_', 1)
    elif css_name.startswith('#'):
        css_name = css_name.replace('#', 'id_', 1)
    else:
        pass
    
    return css_name
        
def render(obj: Any) -> str:
    if hasattr(obj, "__render__"):
        return obj.__render__()
    elif obj is None:
        return "none"  # None requires specific serialization.
    else:
        return f"{obj}"  # Serialize to string


class RenderableObject:
    def __render__(self) -> str:
        pass

    def __add__(self, other: RenderableObject) -> str:  # noqa:F821 https://github.com/PyCQA/pyflakes/issues/373
        return f"{render(self)} {render(other)}"

    def __radd__(self, other: RenderableObject) -> str:  # noqa:F821
        return f"{render(other)} {render(self)}"


class ColorTypes(Enum):
    RGB = 0
    HLS = 1
    HEX = 2


@dataclass
class ColorValue(RenderableObject):
    red: int
    green: int
    blue: int
    typ: ColorTypes = ColorTypes.RGB

    def __render__(self) -> str:
        if self.typ is ColorTypes.RGB:
            return f"rgb({self.red}, {self.green}, {self.blue})"
        elif self.typ is ColorTypes.HLS:
            return f"hls({self.red}, {self.green}%, {self.blue}%)"
        elif self.typ is ColorTypes.HEX:
            return f"#{self.red}{self.green}{self.blue}"
        else:
            raise ValueError("ColorValue type must be a valid ColorTypes attribute")

    def to_hls(self) -> Union[Tuple[float, float, float], NotImplemented]:
        if self.typ is ColorTypes.RGB:
            return rgb_to_hls(self.red, self.green, self.blue)
        else:
            return NotImplemented


@dataclass
class NumericValue(RenderableObject):
    value: Union[float, int]
    unit: str

    def __render__(self) -> str:
        return f"{self.value}{self.unit}"


@dataclass
class Style:
    name: str
    value: Any
    important: bool = False

    def __post_init__(self) -> None:
        self.value = render(self.value)
        f = currentframe().f_back.f_back  # type: ignore
        l, g = f.f_locals, f.f_globals
        if l.get("DARWCSS_AUTO", g.get("DARWCSS_AUTO", False)):
            try:
                selector_name = l.get(
                    "DARWCSS_SELECTOR", g.get("DARWCSS_SELECTOR", "selector")
                )
                selector = l[selector_name]
            except KeyError as exc:
                raise NameError(f"Selector can not found in local namespace.") from exc
            else:
                selector.append(self)


@dataclass
class Selector:
    area: str
    styles: List[Style] = field(default_factory=list)

    def __add__(self, other: Style) -> None:
        self.styles.append(other)

    def __iadd__(self, other: Style) -> Selector: # noqa:F821
        self + other
        return self

    def append(self, other: Style) -> None:
        self.styles.append(other)


class CSS:
    def __init__(self, conf: Optional[Dict] = None) -> None:
        self.selectors: Dict[str, Selector] = {}
        self.conf = conf or {}

    def render(self) -> str:
        css = ""
        for selector in self.selectors.values():
            rules = ""
            for style in selector.styles:
                rules += f"{style.name}: {style.value}{' !important' if style.important else ''};\n"
            css += f"{selector.area}{'{'}\n{indent(rules, ' '*self.conf.get('indent', 4))}{'}'}\n"
        return css

    @contextmanager
    def selector(self, area: str) -> Generator[Selector, None, None]:
        selector = Selector(area)
        try:
            yield selector
        finally:
            self.selectors[clean_name(area)] = selector

    def __getitem__(self, key: str) -> Selector:
        return self.selectors[key]
        
    __call__ = render
    __getattr__ = __getitem__
