from pydantic import BaseModel, Field


class Description(BaseModel):
    value: str
    color: str | None = None
    app_data: dict[str, int] | None = None


class Action(BaseModel):
    link: str | None = None
    name: str


class Tag(BaseModel):
    internal_name: str
    name: str
    category: str
    color: str | None = None
    category_name: str
    localized_tag_name: str | None = None
    localized_category_name: str | None = None


class FilterData(BaseModel):
    player_class_ids: list[str]
    highlight_color: str


class AppData(BaseModel):
    quantity: int | None = None
    def_index: int
    quality: int
    limited: str | None = None
    slot: int | None = None
    filter_data: FilterData | None = None


class EconItem(BaseModel):
    app_id: int | None = Field(default=None, alias="appid")
    context_id: int | None = Field(default=None, alias="contextid")
    asset_id: int | None = Field(default=None, alias="assetid")
    id: int | None = None
    class_id: int | None = Field(default=None, alias="classid")
    instance_id: int = Field(alias="instanceid")
    amount: str | None = None
    pos: int | None = None
    missing: bool | None = None
    currency: int | None = None
    background_color: str
    icon_url: str
    icon_url_large: str
    icon_drag_url: str | None = None
    descriptions: list[Description]
    tradable: int
    actions: list[Action] | None = None
    fraud_warnings: list[str] | None = Field(default=None, alias="fraudwarnings")
    name: str
    name_color: str
    type: str
    market_name: str
    market_hash_name: str
    market_actions: list[Action] | None = None
    commodity: int
    market_tradable_restriction: int
    market_marketable_restriction: int
    marketable: int
    tags: list[Tag]
    app_data: AppData
    owner_descriptions: list[str] | None = None
    owner_actions: list[str] | None = None
