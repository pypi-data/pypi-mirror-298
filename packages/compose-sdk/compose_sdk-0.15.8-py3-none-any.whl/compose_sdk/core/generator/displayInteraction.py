from typing import Union, List
from ..ui import (
    INTERACTION_TYPE,
    TYPE,
    Nullable,
    DISPLAY_UTILS,
    ComponentReturn,
    LanguageName,
    HeaderSize,
)
from ..utils import Utils


class TextComponentReturn(ComponentReturn):
    type: TYPE.DISPLAY_TEXT


def display_text(
    text: Union[
        str,
        int,
        float,
        TextComponentReturn,
        List[Union[str, int, float, TextComponentReturn]],
    ],
    *,
    style: Nullable.Style = None
) -> TextComponentReturn:
    id = Utils.generate_id()

    return {
        "model": {"id": id, "style": style, "properties": {"text": text}},
        "hooks": None,
        "type": TYPE.DISPLAY_TEXT,
        "interactionType": INTERACTION_TYPE.DISPLAY,
    }


def display_header(
    text: str, *, size: HeaderSize = None, style: Nullable.Style = None
) -> ComponentReturn:
    id = Utils.generate_id()

    model_properties = {
        "text": text,
    }

    optional_properties = {
        "size": size,
    }

    for key, value in optional_properties.items():
        if value is not None:
            model_properties[key] = value

    return {
        "model": {"id": id, "style": style, "properties": model_properties},
        "hooks": None,
        "type": TYPE.DISPLAY_HEADER,
        "interactionType": INTERACTION_TYPE.DISPLAY,
    }


def display_json(
    json: DISPLAY_UTILS.Json,
    *,
    label: Nullable.Str = None,
    description: Nullable.Str = None,
    style: Nullable.Style = None
) -> ComponentReturn:
    id = Utils.generate_id()

    return {
        "model": {
            "id": id,
            "style": style,
            "properties": {
                "label": label,
                "description": description,
                "json": json,
            },
        },
        "hooks": None,
        "type": TYPE.DISPLAY_JSON,
        "interactionType": INTERACTION_TYPE.DISPLAY,
    }


def display_spinner(
    *, text: Nullable.Str = None, style: Nullable.Style = None
) -> ComponentReturn:
    id = Utils.generate_id()

    return {
        "model": {
            "id": id,
            "style": style,
            "properties": {
                "text": text,
            },
        },
        "hooks": None,
        "type": TYPE.DISPLAY_SPINNER,
        "interactionType": INTERACTION_TYPE.DISPLAY,
    }


def display_code(
    code: str,
    *,
    label: str = None,
    description: str = None,
    lang: LanguageName = None,
    style: Nullable.Style = None
) -> ComponentReturn:
    id = Utils.generate_id()

    model_properties = {
        "code": code,
    }

    optional_properties = {
        "label": label,
        "description": description,
        "lang": lang,
    }

    for key, value in optional_properties.items():
        if value is not None:
            model_properties[key] = value

    return {
        "model": {
            "id": id,
            "style": style,
            "properties": model_properties,
        },
        "hooks": None,
        "type": TYPE.DISPLAY_CODE,
        "interactionType": INTERACTION_TYPE.DISPLAY,
    }


def display_image(src: str, *, style: Nullable.Style = None) -> ComponentReturn:
    id = Utils.generate_id()

    return {
        "model": {
            "id": id,
            "style": style,
            "properties": {
                "src": src,
            },
        },
        "hooks": None,
        "type": TYPE.DISPLAY_IMAGE,
        "interactionType": INTERACTION_TYPE.DISPLAY,
    }


def display_markdown(markdown: str, *, style: Nullable.Style = None) -> ComponentReturn:
    id = Utils.generate_id()

    return {
        "model": {
            "id": id,
            "style": style,
            "properties": {
                "markdown": markdown,
            },
        },
        "hooks": None,
        "type": TYPE.DISPLAY_MARKDOWN,
        "interactionType": INTERACTION_TYPE.DISPLAY,
    }


def display_none() -> ComponentReturn:
    id = Utils.generate_id()

    return {
        "model": {
            "id": id,
            "style": None,
            "properties": {},
        },
        "hooks": None,
        "type": TYPE.DISPLAY_NONE,
        "interactionType": INTERACTION_TYPE.DISPLAY,
    }
