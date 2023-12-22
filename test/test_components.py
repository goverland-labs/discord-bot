from interactions import ButtonStyle

from src.application.components import ComponentsService, ButtonAction


def test_return_unsubscribe_custom_id():
    assert (
        ComponentsService.get_custom_id(ButtonAction.UNSUBSCRIBE)
        == "f2fd33fc-f62c-44b2-8d4b-58200708ebcd"
    )


def test_unsubscribe_button_created():
    button = ComponentsService.create_button(
        action=ButtonAction.UNSUBSCRIBE,
        style=ButtonStyle.DANGER,
        label="Unsubscribe",
    )
    assert button.custom_id == "f2fd33fc-f62c-44b2-8d4b-58200708ebcd"
    assert button.label == "Unsubscribe"
    assert button.style == ButtonStyle.DANGER
