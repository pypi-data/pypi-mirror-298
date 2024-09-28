import json
import os
from datetime import datetime
from typing import Any, Literal, Optional

import requests
from requests import Response

from models.all import GenericResponseModel, Item, ItemNames, ItemObjects, ItemSkus

BASE_URL: str = "https://schema.autobot.tf/"


class AutobotTF:

    @staticmethod
    def get_schema(
        save_path: str,
        filename: str | None,
    ) -> None:

        if filename is None:
            filename = f"schema_{datetime.now().strftime("%Y%m%d_%H%M%S")}"
        headers = {"accept": "*/*"}
        response = AutobotTF.__make_request(
            method="GET",
            base_url=BASE_URL,
            url="schema/download",
            headers=headers,
            output="json",
        )
        with open(
            os.path.join(save_path, f"{filename}.json"), "w", encoding="utf-8"
        ) as schema:
            json.dump(response, schema, indent=4)

    @staticmethod
    def schema_refresh() -> None:
        AutobotTF.__make_request(
            method="PATCH", base_url="https://schema.autobot.tf/", url="schema/refresh"
        )

    @staticmethod
    def get_schema_key(
        key: Literal[
            "items_game_url",
            "qualities",
            "qualityNames",
            "originNames",
            "attributes",
            "item_sets",
            "attribute_controlled_attached_particles",
            "item_levels",
            "kill_eater_score_types",
            "string_lookups",
            "items",
            "paintkits",
        ]
    ) -> GenericResponseModel:

        headers = {"accept": "*/*"}
        response = AutobotTF.__make_request(
            method="GET",
            base_url=BASE_URL,
            url=f"raw/schema/{key}",
            headers=headers,
            output="json",
        )

        return GenericResponseModel(**response)

    @staticmethod
    def get_schema_property(
        property: Literal[
            "defindexes",
            "qualities",
            "killstreaks",
            "effects",
            "paintkits",
            "wears",
            "crateseries",
            "paints",
            "strangeParts",
            "craftWeapons",
            "uncraftWeapons",
            "craftWeaponsByClass/",
        ],
        class_char: (
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
            | None
        ) = None,
    ) -> GenericResponseModel:

        headers = {"accept": "*/*"}
        response = AutobotTF.__make_request(
            method="GET",
            base_url=f"{BASE_URL}properties/",
            url=(
                property + class_char
                if property == "craftWeaponsByClass/"
                else property
            ),
            headers=headers,
            output="json",
        )

        return GenericResponseModel(value=response)

    @staticmethod
    def get_name(
        items: str | dict | list[str | dict],
        get_from: Literal["item_object", "sku"],
        proper: bool | None = None,
        use_pipe_for_skin: bool | None = None,
    ) -> ItemNames:

        bulk: bool = True if isinstance(items, list) else False
        headers = {"accept": "*/*"}
        params = {
            "proper": (str(proper).lower() if proper is not None else None),
            "usePipeForSkin": (
                str(use_pipe_for_skin).lower()
                if use_pipe_for_skin is not None
                else None
            ),
        }
        if bulk:
            headers["Content-Type"] = "application/json"
        method_mapping = {
            "item_object": "fromItemObjectBulk" if bulk else "fromItemObject",
            "sku": (
                "fromSkuBulk"
                if bulk & AutobotTF.__is_list_of_type(items, str)
                else f"fromSku/{items.replace(";", "%3B")}"
            ),
        }
        from_ = method_mapping.get(get_from)
        response = AutobotTF.__make_request(
            method="GET" if get_from == "sku" and not bulk else "POST",
            base_url=BASE_URL,
            url=f"getName/{from_}",
            params=params,
            headers=headers,
            json=items if get_from != "sku" else None,
            data=items if get_from == "sku" else None,
            output="json",
        )

        return ItemNames(**response)

    @staticmethod
    def get_sku(
        items: str | dict | list[str | dict],
        get_from: Literal["item_object", "name", "econ_item"],
    ) -> ItemSkus:

        bulk: bool = True if isinstance(items, list) else False
        headers = {"accept": "*/*"}
        if bulk:
            headers["Content-Type"] = "application/json"
        method_mapping = {
            "item_object": "fromItemObjectBulk" if bulk else "fromItemObject",
            "name": (
                "fromNameBulk"
                if bulk & AutobotTF.__is_list_of_type(items, str)
                else f"fromName/{items}"
            ),
            "econ_item": (
                "fromEconItemBulk"
                if bulk & AutobotTF.__is_list_of_type(items, dict)
                else "fromEconItem"
            ),
        }
        from_ = method_mapping.get(get_from)
        response = AutobotTF.__make_request(
            method="GET" if get_from == "sku" and not bulk else "POST",
            base_url=BASE_URL,
            url=f"getSku/{from_}",
            headers=headers,
            json=items,
            output="json",
        )

        return ItemSkus(**response)

    @staticmethod
    def get_item_object(
        items: str | dict | list[str | dict],
        get_from: Literal["name", "sku", "econ_item"],
        normalize_festivized_items: bool | None = None,
        normalize_strange_2nd_quality: bool | None = None,
        normalize_painted: bool | None = None,
    ) -> ItemObjects:

        bulk: bool = True if isinstance(items, list) else False
        if isinstance(items, dict) | AutobotTF.__is_list_of_type(items, dict):
            return AutobotTF.__from_econ_items(items, bulk)
        headers = {"accept": "*/*"}
        if bulk:
            headers["Content-Type"] = "application/json"

        params = {
            "normalizeFestivizedItems": (
                str(normalize_festivized_items).lower()
                if normalize_festivized_items is not None
                else None
            ),
            "normalizeStrangeAsSecondQuality": (
                str(normalize_strange_2nd_quality).lower()
                if normalize_strange_2nd_quality is not None
                else None
            ),
            "normalizedPainted": (
                str(normalize_painted).lower()
                if normalize_painted is not None
                else None
            ),
        }
        method_mapping = {
            "name": "fromNameBulk" if bulk else f"fromName/{items}",
            "sku": "fromSkuBulk" if bulk else f"fromSku/{items.replace(";", "%3B")}",
        }
        from_ = method_mapping.get(get_from)
        response = AutobotTF.__make_request(
            method="POST" if bulk else "GET",
            base_url=BASE_URL,
            url=f"getItemObject/{from_}",
            params=params,
            headers=headers,
            json=items if bulk else None,
            output="json",
        )

        return ItemObjects(**response)

    @staticmethod
    def get_item_grade(
        items: int | str | None = None,
        get_from: Literal["def_index", "name", "sku"] | None = None,
    ) -> GenericResponseModel:

        headers = {"accept": "*/*"}
        method_mapping = {
            "def_index": f"fromDefindex/{items}",
            "name": f"fromName/{items}",
            "sku": f"fromSku/{items}",
        }
        from_ = method_mapping.get(get_from)
        response = AutobotTF.__make_request(
            method="GET",
            base_url=BASE_URL,
            url=f"getItemGrade/{from_}",
            headers=headers,
            output="json",
        )

        return GenericResponseModel(**response)

    @staticmethod
    def get_item_grades(v: Literal["v1", "v2"]) -> GenericResponseModel:

        headers = {"accept": "*/*"}
        response = AutobotTF.__make_request(
            method="GET",
            base_url=BASE_URL,
            url=f"getItemGrade/{v}",
            headers=headers,
            output="json",
        )

        return GenericResponseModel(**response)

    @staticmethod
    def get_item(
        items: str | int, get_from: Literal["def_index", "name", "sku"]
    ) -> Item:

        headers = {"accept": "*/*"}
        method_mapping = {
            "def_index": f"getItem/fromDefindex/{items}",
            "name": f"getItem/fromName/{items}",
            "sku": f"getItem/fromSku/{items}",
        }
        response = AutobotTF.__make_request(
            method="GET",
            base_url=BASE_URL,
            url=method_mapping.get(get_from),
            headers=headers,
            output="json",
        )

        return Item(**response)

    @staticmethod
    def __make_request(
        method: Literal["GET", "POST", "PATCH"],
        base_url: str,
        url: str,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        data: dict | list | None = None,
        json: dict | list | None = None,
        output: Literal["raw", "txt", "json"] | None = "raw",
    ) -> Response | str | dict:

        try:
            response: Response = requests.request(
                method=method,
                url=base_url + url,
                params=params,
                data=data,
                json=json,
                headers=headers,
            )
            response.raise_for_status()

            if output == "raw":
                return response
            elif output == "txt":
                return response.text
            elif output == "json":
                return response.json()

        except requests.HTTPError as e:
            print(f"HTTP ERROR : {e}")
        except requests.ConnectionError as e:
            print(f"CONNECTION ERROR : {e}")

    @staticmethod
    def __is_list_of_type(obj, of_: Any):
        return isinstance(obj, list) & all(isinstance(item, of_) for item in obj)

    @staticmethod
    def __from_econ_items(items: dict | list[dict], bulk: bool) -> ItemObjects:

        headers = {
            "accept": "*/*",
            "Content-Type": "application/json",
        }
        response = AutobotTF.__make_request(
            method="POST",
            base_url=f"{BASE_URL}getItemObject/",
            url="fromEconItem" if not bulk else "fromEconItemBulk",
            headers=headers,
            json=items,
            output="json",
        )

        return ItemObjects(**response)
