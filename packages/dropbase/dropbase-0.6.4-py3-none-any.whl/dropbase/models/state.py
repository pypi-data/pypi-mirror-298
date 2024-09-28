from datetime import date, datetime, time
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel


# state models
class PageState(BaseModel):
    message: Optional[str] = None
    message_status: Optional[Literal["success", "warning", "error", "info"]] = None
    message_description: Optional[str] = None


class BaseStateBlock(BaseModel):
    visible: Optional[bool] = None


class TableEdits(BaseModel):
    old: Optional[Dict] = None
    new: Optional[Dict] = None
    columns: Optional[List] = None


class TableSelected(BaseModel):
    values: Optional[List[Dict]] = []
    rows: Optional[List[Dict]] = []


class TableState(BaseStateBlock):
    data: Optional[List] = []
    selected: Optional[TableSelected] = {}
    edits: Optional[Dict[str, TableEdits]] = {}


class ChartSelection(BaseModel):
    x: Optional[Any] = None
    y: Optional[Any] = None
    curve_number: Optional[Any] = None
    point_number: Optional[Any] = None


class ChartState(BaseStateBlock):
    data: Optional[Any] = None
    selected: Optional[ChartSelection] = None


class StrInputState(BaseStateBlock):
    value: Optional[str] = None


class IntInputState(BaseStateBlock):
    value: Optional[int] = None


class FloatInputState(BaseStateBlock):
    value: Optional[float] = None


class DateTimeInputState(BaseStateBlock):
    value: Optional[datetime] = None


class DateInputState(BaseStateBlock):
    value: Optional[date] = None


class TimeInputState(BaseStateBlock):
    value: Optional[time] = None


class TextareaState(BaseModel):
    visible: Optional[bool] = None
    value: Optional[str] = None


# maybe reuse one from models
class SelectOption(BaseModel):
    text: Optional[str] = None
    value: Optional[Any] = None


class SelectState(BaseStateBlock):
    value: Optional[str] = None
    options: Optional[List[Union[str, SelectOption]]] = []


class ButtonState(BaseStateBlock):
    pass


class TextState(BaseStateBlock):
    text: Optional[str] = None


class BooleanState(BaseStateBlock):
    value: Optional[bool] = None
