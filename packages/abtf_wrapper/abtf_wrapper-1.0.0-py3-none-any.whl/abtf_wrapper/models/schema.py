from typing import Literal

from pydantic import BaseModel, Field


class ItemAttribute(BaseModel):
    name: str
    def_index: int = Field(alias="defindex")
    attribute_class: str | None = None
    description_string: str | None = None
    description_format: str | None = None
    effect_type: Literal[
        "positive",
        "negative",
        "neutral",
        "unusual",
        "strange",
        "value_is_from_lookup_table",
    ]
    hidden: bool
    stored_as_integer: bool


class Origin(BaseModel):
    index: int = Field(alias="origin")
    name: str


class Attribute(BaseModel):
    name: str
    attr_class: str = Field(alias="class")
    value: int | float


class Set(BaseModel):
    item_set: str
    name: str
    items: list[str]
    attributes: list[Attribute] | None = None


class Particle(BaseModel):
    system: str
    id: int
    attach_to_rootbone: bool
    name: str


class Level(BaseModel):
    level: int
    required_score: int
    name: str


class LevelName(BaseModel):
    name: str
    levels: list[Level]


class Counter(BaseModel):
    type: int
    type_name: str
    level_data: str


class String(BaseModel):
    index: int
    string: str


class TableName(BaseModel):
    table_name: str
    strings: list[String]


class StringLookups(BaseModel):
    success: bool
    table_names: list[TableName] = Field(alias="value")


class Capability(BaseModel):
    nameable: bool | None = None
    can_gift_wrap: bool | None = None
    can_craft_mark: bool | None = None
    can_be_restored: bool | None = None
    strange_parts: bool | None = None
    can_card_upgrade: bool | None = None
    can_strangify: bool | None = None
    can_killstreakify: bool | None = None
    can_consume: bool | None = None


class SchemaItem(BaseModel):
    name: str
    def_index: int = Field(alias="defindex")
    item_class: str
    item_type_name: str
    item_name: str
    proper_name: bool
    item_slot: str | None = None
    player_model: str | None = Field(alias="model_player", default=None)
    item_quality: int
    image_inventory: str
    min_item_level: int = Field(ge=1, le=100, alias="min_ilevel")
    max_item_level: int = Field(ge=1, le=100, alias="max_ilevel")
    image_url: str
    image_url_large: str
    drop_type: Literal["none", "drop"] | None = None
    craft_class: str
    craft_material_type: str
    capabilities: Capability
    styles: list[dict[str, str]] | None = None
    used_by_classes: list[
        Literal[
            "Scout",
            "Soldier",
            "Pyro",
            "Demoman",
            "Heavy",
            "Engineer",
            "Medic",
            "Sniper",
            "Spy",
        ]
    ]
    attributes: list[Attribute] | None = None
