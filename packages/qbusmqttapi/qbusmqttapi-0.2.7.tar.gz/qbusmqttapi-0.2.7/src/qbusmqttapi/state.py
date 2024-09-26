"""Qbus state models."""

from enum import StrEnum
from typing import Any
from .const import (
    KEY_OUTPUT_ACTION,
    KEY_OUTPUT_ID,
    KEY_OUTPUT_PROPERTIES,
    KEY_OUTPUT_TYPE,
    KEY_PROPERTIES_VALUE,
)

KEY_CONTROLLER_CONNECTABLE = "connectable"
KEY_CONTROLLER_CONNECTED = "connected"
KEY_CONTROLLER_ID = "id"
KEY_CONTROLLER_STATE_PROPERTIES = "properties"


class StateType(StrEnum):
    """Values to be used as state type."""

    ACTION = "action"
    STATE = "state"


class StateAction(StrEnum):
    """Values to be used as state action."""

    ACTIVATE = "activate"
    ACTIVE = "active"


class QbusMqttControllerStateProperties:
    """MQTT representation a Qbus controller its state properties."""

    def __init__(self, data: dict) -> None:
        """Initialize based on a json loaded dictionary."""
        self.connectable: bool | None = data.get(KEY_CONTROLLER_CONNECTABLE)
        self.connected: bool | None = data.get(KEY_CONTROLLER_CONNECTED)


class QbusMqttControllerState:
    """MQTT representation of a Qbus controller state."""

    def __init__(self, data: dict) -> None:
        """Initialize based on a json loaded dictionary."""
        self.id: str | None = data.get(KEY_CONTROLLER_ID)

        properties = data.get(KEY_CONTROLLER_STATE_PROPERTIES)
        self.properties: QbusMqttControllerStateProperties | None = (
            QbusMqttControllerStateProperties(properties)
            if properties is not None
            else None
        )


class QbusMqttState:
    """MQTT representation of a Qbus state."""

    def __init__(
        self,
        data: dict | None = None,
        *,
        id: str | None = None,
        type: str | None = None,
        action: str | None = None,
    ) -> None:
        """Initialize state."""
        self.id: str = ""
        self.type: str = ""
        self.action: str | None = None
        self.properties: dict | None = None

        if data is not None:
            self.id = data.get(KEY_OUTPUT_ID, "")
            self.type = data.get(KEY_OUTPUT_TYPE, "")
            self.action = data.get(KEY_OUTPUT_ACTION)
            self.properties = data.get(KEY_OUTPUT_PROPERTIES)

        if id is not None:
            self.id = id

        if type is not None:
            self.type = type

        if action is not None:
            self.action = action

    def read_property(self, key: str, default: Any) -> Any:
        """Read a property."""
        return self.properties.get(key, default) if self.properties else default

    def write_property(self, key: str, value: Any) -> None:
        """Add or update a property."""
        if self.properties is None:
            self.properties = {}

        self.properties[key] = value


class QbusMqttOnOffState(QbusMqttState):
    """MQTT representation of a Qbus on/off output."""

    def __init__(
        self,
        data: dict | None = None,
        *,
        id: str | None = None,
        type: str | None = None,
    ) -> None:
        super().__init__(data, id=id, type=type)

    def read_value(self) -> bool:
        """Read the value of the Qbus output."""
        return self.read_property(KEY_PROPERTIES_VALUE, False)

    def write_value(self, value: bool) -> None:
        """Set the value of the Qbus output."""
        self.write_property(KEY_PROPERTIES_VALUE, value)


class QbusMqttAnalogState(QbusMqttState):
    """MQTT representation of a Qbus analog output."""

    def __init__(
        self,
        data: dict | None = None,
        *,
        id: str | None = None,
        type: str | None = None,
    ) -> None:
        super().__init__(data, id=id, type=type)

    def read_percentage(self) -> float:
        """Read the value of the Qbus output."""
        return self.read_property(KEY_PROPERTIES_VALUE, 0)

    def write_percentage(self, percentage: float) -> None:
        """Set the value of the Qbus output."""
        self.write_property(KEY_PROPERTIES_VALUE, percentage)
