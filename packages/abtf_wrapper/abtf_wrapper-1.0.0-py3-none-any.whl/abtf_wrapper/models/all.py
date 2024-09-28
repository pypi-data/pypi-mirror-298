from pydantic import AliasChoices, BaseModel, Field

from models.econ_item import EconItem
from models.item_object import ItemObject
from models.items_game import ItemsGameItems
from models.schema import (
    Attribute,
    Counter,
    ItemAttribute,
    LevelName,
    Origin,
    Particle,
    SchemaItem,
    Set,
    StringLookups,
)


class ItemNames(BaseModel):
    success: bool
    names: str | list[str] = Field(validation_alias=AliasChoices("name", "itemNames"))


class ItemSkus(BaseModel):
    success: bool
    skus: str | list[str] = Field(validation_alias=AliasChoices("sku", "skus"))


class ItemObjects(BaseModel):
    success: bool
    item_objects: ItemObject | list[ItemObject] = Field(
        validation_alias=AliasChoices("item", "itemObject", "itemObjects")
    )


class EconItems(BaseModel):
    econ_items: list[EconItem]


class GenericResponseModel(BaseModel):
    success: bool | None = None
    values: (
        str
        | int
        | list[
            str
            | ItemAttribute
            | Origin
            | Attribute
            | Set
            | Particle
            | LevelName
            | Counter
            | StringLookups
        ]
        | dict[str | int, str | int]
    ) = Field(validation_alias=(AliasChoices("value", "grade", "items")))


class Item(BaseModel):
    success: bool
    schema_items: SchemaItem = Field(alias="schemaItems")
    items_game_items: ItemsGameItems = Field(alias="items_gameItems")
