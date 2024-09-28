from datetime import datetime

from pydantic import BaseModel, Field


class Rarity(BaseModel):
    value: int
    loc_key: str
    loc_key_weapon: str
    color: str
    loot_list: str | None = None
    drop_sound: str | None = None
    next_rarity: str | None = None


class ConditionLogic(BaseModel):
    type: str
    value: str | None = None
    player_key: str | None = None
    get_player: str | None = None
    is_owner: int | None = None
    team_key: str | None = None
    team_requirement: int | None = None
    distance_check_type: int | None = None
    distance_to_check: int | None = None
    key_to_lookup: str | None = None


class Quest(BaseModel):
    name: str
    condition_logic: dict[str, dict[str, ConditionLogic]]
    type: str
    event_name: str | None = None
    score_key_name: str | None = None


class QuestObjectiveConditions(BaseModel):
    success: bool
    value: dict[str, Quest]


class CardType(BaseModel):
    value: int
    loc_key: str
    ui: str


class ItemCollection(BaseModel):
    name: str
    description: str
    is_reference_collection: int
    items: dict[str, int | dict[str, int]]


class Operation(BaseModel):
    name: str
    operation_start_date: datetime
    stop_adding_to_queue_date: datetime
    stop_giving_to_player_date: datetime
    contracts_end_date: datetime
    operation_loot_list: str = Field(alias="operation_lootlist")
    is_campaign: int | None = None
    max_drop_count: int | None = None
    uses_credits: int | None = None


class CapabilityExt(BaseModel):
    can_craft_count: bool | None = None
    paintable: bool | None = None


class Tool(BaseModel):
    type: str
    usage_capabilities: dict[str, bool]
    restriction: str


class Tag(BaseModel):
    can_deal_damage: bool | None = None
    can_deal_mvm_penetration_damage: bool | None = None
    can_deal_long_distance_damage: bool | None = None


class PlayerBodyGroup(BaseModel):
    hat: bool | None = None
    head: bool | None = None
    headphones: bool | None = None
    grenades: bool | None = None
    dog_tags: bool | None = Field(alias="dogtags", default=None)
    backpack: bool | None = None
    shoes: bool | None = None
    shoes_socks: bool | None = None


class AdditionalHiddenBodyGroup(BaseModel):
    hat: bool | None = None
    head: bool | None = None
    headphones: bool | None = None
    grenades: bool | None = None
    dog_tags: bool | None = Field(alias="dogtags", default=None)


class Style(BaseModel):
    name: str | None = None
    player_model: str | None = Field(default=None, alias="model_player")
    additional_hidden_body_groups: AdditionalHiddenBodyGroup = Field(
        alias="additional_hidden_bodygroups", default=None
    )
    player_model_per_class: dict[str, str] | None = Field(
        default=None, alias="model_player_per_class"
    )
    skin_red: bool | None = None
    skin_blu: bool | None = None


class Visuals(BaseModel):
    player_body_groups: PlayerBodyGroup | None = Field(
        alias="player_bodygroups", default=None
    )
    styles: dict[int, Style] | None = None
    custom_particle_system: dict[str, str] | None = Field(
        alias="custom_particlesystem", default=None
    )
    sound_deploy: str | None = None


class StaticAttr(BaseModel):
    set_supply_crate_series: int | None = Field(
        alias="set supply crate series", default=None
    )
    hide_crate_series_number: bool | None = Field(
        alias="hide crate series numbers", default=None
    )
    decoded_by_item_def_index: int | None = Field(
        alias="decoded by itemdefindex", default=None
    )
    weapon_allow_inspect: bool | None = None
    item_style_override: bool | None = Field(alias="item style override", default=None)
    is_winter_case: bool | None = Field(alias="is winter case", default=None)
    is_marketable: bool | None = Field(alias="is marketable", default=None)
    is_commodity: bool | None = Field(alias="is commodity", default=None)
    kill_eater_score_type: int | None = Field(
        alias="kill eater score type", default=None
    )
    kill_eater_score_type_2: int | None = Field(
        alias="kill eater score type 2", default=None
    )
    kill_eater_score_type_3: int | None = Field(
        alias="kill eater score type 3", default=None
    )
    cannot_trade: bool | None = Field(alias="cannot trade", default=None)
    is_operation_pass: bool | None = None
    style_changes_on_strange_level: int | None = Field(
        alias="style changes on strange level", default=None
    )
    cannot_restore: bool | None = Field(alias="cannot restore", default=None)
    cannot_giftwrap: bool | None = Field(alias="cannot giftwrap", default=None)
    always_transmit_so: bool | None = None
    never_craftable: bool | None = Field(alias="never craftable", default=None)
    deactive_date: int | None = Field(alias="deactive date", default=None)
    paintkit_proto_def_index: int | None = None
    has_team_color_paintkit: bool | None = None
    limited_quantity_item: bool | None = Field(
        alias="limited quantity item", default=None
    )
    is_giger_counter: bool | None = Field(alias="is giger counter", default=None)
    min_viewmodel_offset: str | None = None
    inspect_viewmodel_offset: str | None = None
    item_meter_charge_type: int | None = None
    item_meter_charge_rate: float | None = None
    meter_label: str | None = None
    mult_player_movespeed_active: float | None = None
    mod_maxhealth_drain_rate: float | None = None
    energy_weapon_no_ammo: bool | None = None
    energy_weapon_charged_shot: bool | None = None
    energy_weapon_no_hurt_building: bool | None = None
    crits_become_minicrits: bool | None = None
    crit_mod_disabled: bool | None = None
    always_tradable: bool | None = None
    tool_target_item: int | None = Field(alias="tool target item", default=None)


class ItemsGameItems(BaseModel):
    name: str
    first_sale_date: str | None = None
    prefab: str | None = None
    baseitem: int | None = None
    capabilities: CapabilityExt | None = None
    equip_regions: dict[str, int] | None = None
    proper_name: bool | None = Field(alias="propername", default=None)
    min_item_level: int | None = Field(alias="min_ilevel", default=None)
    max_item_level: int | None = Field(alias="max_ilevel", default=None)
    hidden: bool | None = None
    inspect_panel_dist: int | None = None
    item_name: str | None = None
    item_type_name: str | None = None
    item_slot: str | None = None
    item_quality: str | None = None
    image_inventory: str | None = None
    image_inventory_size_w: int | None = None
    image_inventory_size_h: int | None = None
    craft_class: str | None = None
    craft_material_type: str | None = None
    player_model: str | None = Field(alias="model_player", default=None)
    attach_to_hands: int | None = None
    drop_type: str | None = None
    used_by_classes: dict[str, bool | str] | None = None
    mouse_pressed_sound: str | None = None
    drop_sound: str | None = None
    tags: Tag | None = None
    ad_text: str | None = None
    default_skin: int | None = None
    static_attrs: StaticAttr | None = None
    xifier_class_remap: str | None = None
