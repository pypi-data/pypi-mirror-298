from typing import Any, Callable, List, Literal, Optional, Union

from pydantic import BaseModel


class BaseBlock(BaseModel):
    id: str
    visible: bool
    label: Optional[str] = None
    w: int = 2
    h: int = 1
    x: int = 0
    y: int = 0


class Text(BaseBlock):
    block_type: Literal["Text"] = "Text"
    text: Optional[str] = None


class Boolean(BaseBlock):
    block_type: Literal["Boolean"] = "Boolean"
    on_toggle: Optional[Callable] = None


class Input(BaseBlock):
    on_enter: Optional[Callable] = None
    block_type: Literal["Input"] = "Input"
    data_type: Literal["str", "int", "float", "datetime", "date", "time"] = "str"


class Textarea(BaseBlock):
    block_type: Literal["Textarea"] = "Textarea"


# NOTE: SelectOption is a duplicate of state, might need to refactor later
class SelectOption(BaseModel):
    text: Optional[str] = None
    value: Optional[Any] = None


class Select(BaseBlock):
    options: Optional[List[Union[SelectOption, str]]] = []
    on_change: Optional[Callable] = None
    block_type: Literal["Select"] = "Select"


class Button(BaseBlock):
    on_click: Optional[Callable] = None
    block_type: Literal["Button"] = "Button"


class Chart(BaseBlock):
    block_type: Literal["Chart"] = "Chart"
    on_chart_click: Optional[Callable] = None
    # refetch_interval: Optional[int] = None


class BaseColumn(BaseModel):
    id: str
    name: Optional[str] = None
    editable: Optional[bool] = False
    visible: Optional[bool] = False


class BoolColumn(BaseColumn):
    block_type: Literal["BoolColumn"] = "BoolColumn"
    data_type: Literal["bool"] = "bool"


class Column(BaseColumn):
    block_type: Literal["Column"] = "Column"
    data_type: Literal["str", "int", "float", "datetime", "date", "time"] = "str"
    # index: bool = False


class PossibleTag(BaseModel):
    tag: str
    color: str


class TagColumn(BaseColumn):
    block_type: Literal["TagColumn"] = "TagColumn"
    data_type: Literal["str"] = "str"
    possible_tags: Optional[List[PossibleTag]] = []


class SelectColumn(BaseColumn):
    block_type: Literal["SelectColumn"] = "SelectColumn"
    data_type: Literal["str"] = "str"
    options: Optional[List[str]] = []


class MultiSelectColumnOption(BaseModel):
    value: str
    color: Optional[str] = None


class MultiSelectColumn(BaseColumn):
    block_type: Literal["MultiSelectColumn"] = "MultiSelectColumn"
    data_type: Literal["list"] = "list"
    options: Optional[List[Union[str, MultiSelectColumnOption]]] = []


TableColumnModels = Union[Column, SelectColumn, MultiSelectColumn, BoolColumn, TagColumn]


class Table(BaseBlock):
    on_row_change: Optional[Callable] = None
    columns: Optional[List[TableColumnModels]] = []
    block_type: Literal["Table"] = "Table"


class Page(BaseModel):
    id: str
    name: str
    on_load: Optional[Callable] = None
    blocks: tuple[
        Union[Text, Boolean, Input, Textarea, Select, Button, Table, Chart],
        ...,
    ]


AvailablePageBlock = [Text, Boolean, Input, Textarea, Select, Button, Table, Chart]
