from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

TagAttributes = Dict[str, str]
Tags = Dict[str, TagAttributes]

class Segment:
    def __init__(self, id: str, text: str, tags: Optional[Tags] = None):
        self.id = id
        self.text = text
        self.tags = tags if tags is not None else {}

class LayoutNode:
    def __init__(self, type: str):
        self.type = type

class LayoutSegment(LayoutNode):
    def __init__(self, id: str):
        LayoutNode.__init__(self, 'segment')
        self.id = id

class LayoutElement(LayoutNode):
    def __init__(self, type: str, tagName: str, children: List[Union['LayoutElement', 'LayoutSegment']], value: Optional[str] = None, tags: Optional[Tags] = None, properties: Optional[Dict] = None):
        LayoutNode.__init__(self, type)
        self.value = value
        self.tagName = tagName
        self.children = children
        self.properties = properties if properties is not None else {}

class LayoutRoot(LayoutNode):
    def __init__(self, children: List[LayoutElement | LayoutSegment]):
        LayoutNode.__init__(self, 'root')
        self.children = children

Context = Dict

class Document:
    def __init__(self, segments: List[Segment], layout: LayoutRoot, metadata: Optional[Dict] = None):
        self.segments = segments
        self.layout = layout
        self.metadata = metadata if metadata is not None else {}

class Processor(ABC):
    @abstractmethod
    def parse(self, res: str, ctx: Context) -> Document:
        pass

    @abstractmethod
    def stringify(self, doc: Document, ctx: Context) -> str:
        pass
