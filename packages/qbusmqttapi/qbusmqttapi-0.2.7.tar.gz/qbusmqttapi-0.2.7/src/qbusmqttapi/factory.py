"""Qbus MQTT factory."""

from dataclasses import dataclass
import json
import logging
from typing import Any, TypeVar

from .const import (
    KEY_PROPERTIES_AUTHKEY,
    TOPIC_PREFIX,
)
from .discovery import QbusDiscovery, QbusMqttDevice
from .state import (
    QbusMqttControllerState,
    QbusMqttState,
    StateAction,
    StateType,
)

_LOGGER = logging.getLogger(__name__)


@dataclass
class QbusMqttRequestMessage:
    """Qbus MQTT request data class."""

    topic: str
    payload: str | bytes


class QbusMqttMessageFactory:
    """Factory methods for Qbus MQTT messages."""

    T = TypeVar("T", bound="QbusMqttState")

    def __init__(self) -> None:
        self._topic_factory = QbusMqttTopicFactory()

    def parse_discovery(self, payload: str | bytes) -> QbusDiscovery | None:
        """Parse an MQTT message and return an instance
        of QbusDiscovery if successful, otherwise None."""

        discovery: QbusDiscovery | None = self.deserialize(QbusDiscovery, payload)

        # Discovery data must include the Qbus device type and name.
        if discovery is not None and len(discovery.devices) == 0:
            _LOGGER.error("Incomplete discovery payload: %s", payload)
            return None

        return discovery

    def parse_controller_state(
        self, payload: str | bytes
    ) -> QbusMqttControllerState | None:
        """Parse an MQTT message and return an instance
        of QbusMqttControllerState if successful, otherwise None."""

        return self.deserialize(QbusMqttControllerState, payload)

    def parse_output_state(self, cls: type[T], payload: str | bytes) -> T | None:
        """Parse an MQTT message and return an instance
        of T if successful, otherwise None."""

        return self.deserialize(cls, payload)

    def create_device_activate_request(
        self, device: QbusMqttDevice, prefix: str = TOPIC_PREFIX
    ) -> QbusMqttRequestMessage:
        """Create a message to request device activation."""
        state = QbusMqttState(
            id=device.id, type=StateType.ACTION, action=StateAction.ACTIVATE
        )
        state.write_property(KEY_PROPERTIES_AUTHKEY, "ubielite")

        return QbusMqttRequestMessage(
            self._topic_factory.get_device_command_topic(device.id, prefix),
            self.serialize(state),
        )

    def create_device_state_request(
        self, device: QbusMqttDevice, prefix: str = TOPIC_PREFIX
    ) -> QbusMqttRequestMessage:
        """Create a message to request a device state."""
        return QbusMqttRequestMessage(
            self._topic_factory.get_get_state_topic(prefix), json.dumps([device.id])
        )

    def create_state_request(
        self, entity_ids: list[str], prefix: str = TOPIC_PREFIX
    ) -> QbusMqttRequestMessage:
        """Create a message to request entity states."""
        return QbusMqttRequestMessage(
            self._topic_factory.get_get_state_topic(prefix), json.dumps(entity_ids)
        )

    def create_set_output_state_request(
        self, device: QbusMqttDevice, state: QbusMqttState, prefix: str = TOPIC_PREFIX
    ) -> QbusMqttRequestMessage:
        """Create a message to update the output state."""
        return QbusMqttRequestMessage(
            self._topic_factory.get_output_command_topic(device.id, state.id, prefix),
            self.serialize(state),
        )

    def serialize(self, obj: Any) -> str:
        """Convert an object to json payload."""
        return json.dumps(obj, cls=IgnoreNoneJsonEncoder)

    def deserialize(self, state_cls: type[Any], payload: str | bytes) -> Any | None:
        """Parse an MQTT message and return the requested type if successful, otherwise None."""

        if payload is None:
            _LOGGER.warning("Empty state payload for %s", state_cls.__name__)
            return None

        try:
            data = json.loads(payload)
        except ValueError:
            _LOGGER.error(
                "Invalid state payload for %s: %s", state_cls.__name__, payload
            )
            return None

        return state_cls(data)


class QbusMqttTopicFactory:
    """Factory methods for topics of the Qbus MQTT API."""

    def get_get_config_topic(self, prefix: str = TOPIC_PREFIX) -> str:
        """Return the getConfig topic."""
        return f"{prefix}/getConfig"

    def get_config_topic(self, prefix: str = TOPIC_PREFIX) -> str:
        """Return the config topic."""
        return f"{prefix}/config"

    def get_get_state_topic(self, prefix: str = TOPIC_PREFIX) -> str:
        """Return the getState topic."""
        return f"{prefix}/getState"

    def get_device_state_topic(self, device_id: str, prefix: str = TOPIC_PREFIX) -> str:
        """Return the state topic."""
        return f"{prefix}/{device_id}/state"

    def get_device_command_topic(
        self, device_id: str, prefix: str = TOPIC_PREFIX
    ) -> str:
        """Return the 'set state' topic."""
        return f"{prefix}/{device_id}/setState"

    def get_output_command_topic(
        self, device_id: str, entity_id: str, prefix: str = TOPIC_PREFIX
    ) -> str:
        """Return the 'set state' topic of an output."""
        return f"{prefix}/{device_id}/{entity_id}/setState"

    def get_output_state_topic(
        self, device_id: str, entity_id: str, prefix: str = TOPIC_PREFIX
    ) -> str:
        """Return the state topic of an output."""
        return f"{prefix}/{device_id}/{entity_id}/state"


class IgnoreNoneJsonEncoder(json.JSONEncoder):
    """A json encoder to ignore None values when serializing."""

    def default(self, o):
        if hasattr(o, "__dict__"):
            # Filter out None values
            return {k: v for k, v in o.__dict__.items() if v is not None}
        return super().default(o)
