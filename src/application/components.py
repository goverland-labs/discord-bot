import uuid
from typing import Optional

from interactions import ButtonStyle, Button, Emoji, StrEnum


class ButtonAction(StrEnum):
    UNSUBSCRIBE = ("UNSUBSCRIBE",)
    SUBSCRIBE = ("SUBSCRIBE",)


"""
Global registry of all actions and corresponding custom ids.
This dict contains a pair of Action and UUID of a custom ID, e.g.
"UNSUBSCRIBE" -> "f2fd33fc-f62c-44b2-8d4b-58200708ebcd".

You can query the custom id by the action later on.
"""
COMPONENTS_REGISTRY = {
    ButtonAction.UNSUBSCRIBE: "f2fd33fc-f62c-44b2-8d4b-58200708ebcd",
    ButtonAction.SUBSCRIBE: "3ac23da1-e679-4c75-b023-63b9ca277498",
}


class ComponentsService:
    @staticmethod
    def get_custom_id(action):
        return COMPONENTS_REGISTRY.get(action.value, None)

    @staticmethod
    def create_button(
        style: ButtonStyle,
        label: str,
        action: ButtonAction,
        emoji: Optional[Emoji] = None,
        url: Optional[str] = None,
        disabled: Optional[bool] = None,
    ):
        return Button(
            style=style,
            label=label,
            emoji=emoji,
            url=url,
            disabled=disabled,
            custom_id=ComponentsService.get_custom_id(action),
            value="PUSHA",
        )
