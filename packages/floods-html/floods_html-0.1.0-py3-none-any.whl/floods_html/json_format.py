from pydantic import BaseModel, field_serializer, model_validator
from pydantic_extra_types.color import Color
from pydantic_core import SchemaValidator

from typing import List, Literal, Union, Optional


def check_schema(model: BaseModel) -> None:
    schema_validator = SchemaValidator(schema=model.__pydantic_core_schema__)
    schema_validator.validate_python(model.__dict__)


class FHTableEntry(BaseModel):
    value: Union[str, int, float, None]
    background_color: Optional[Color] = None

    @field_serializer("background_color")
    def serialize_color(self, background_color, _info):
        return background_color.as_hex("Long") if background_color is not None else None


class FHTable(BaseModel):
    title: str
    header: List[FHTableEntry] = []
    rows: List[List[FHTableEntry]] = []

    @model_validator(mode="after")
    def rows_wrong_size(self):
        header_len = len(self.header)
        if header_len != 0 and len(self.rows) != 0:
            for row in self.rows:
                if len(row) != header_len:
                    raise ValueError("row lengths do not match header")
        return self

    def add_row(self, row: List[FHTableEntry]):
        self.rows.append(row)
        check_schema(self)

    def add_header(self, header: List[FHTableEntry]):
        self.header = header
        check_schema(self)


class FHFigure(BaseModel):
    title: str
    filename: str
    width: Optional[Union[int, float, str]] = None
    height: Optional[Union[int, float, str]] = None


class FHObject(BaseModel):
    type: Literal["table", "svg_figure"]
    data: Union[FHTable, FHFigure]


class FHJSON(BaseModel):
    data: List[FHObject] = []

    def add_table(self, table):
        self.data.append(FHObject(type="table", data=table))
        check_schema(self)

    def add_svg_figure(self, figure):
        self.data.append(FHObject(type="svg_figure", data=figure))
        check_schema(self)
