from pydantic import BaseModel, Field


class ItemObject(BaseModel):
    def_index: int = Field(alias="defindex")
    quality: int
    craftable: bool
    tradable: bool
    killstreak: int
    australium: bool
    effect: int | None = None
    festive: bool
    paint_kit: int | None = Field(alias="paintkit", default=None)
    wear: int | None = None
    quality2: int | None = None
    craft_number: int | None = Field(alias="craftnumber", default=None)
    crate_series: int | None = Field(alias="crateseries", default=None)
    target: int | None = None
    output: int | None = None
    output_quality: int | None = Field(alias="outputQuality", default=None)
    paint: int | None = None
