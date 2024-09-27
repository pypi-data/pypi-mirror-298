"""HSMS settings class."""
from __future__ import annotations

import enum

import secsgem_cyg.common


class HsmsConnectMode(enum.Enum):
    """Hsms connect mode (active or passive)."""

    ACTIVE = 1
    PASSIVE = 2

    def __repr__(self) -> str:
        """String representation of object."""
        return "Active" if self == self.ACTIVE else "Passive"


class HsmsSettings(secsgem_cyg.common.Settings):
    """Settings for HSMS connection.

    These attributes can be initialized in the constructor and accessed as property.

    Example:
        >>> import secsgem_cyg.hsms
        >>>
        >>> settings = secsgem_cyg.hsms.HsmsSettings(device_type=secsgem_cyg.common.DeviceType.EQUIPMENT)
        >>> settings.device_type
        <DeviceType.EQUIPMENT: 0>
        >>> settings.address
        '127.0.0.1'

    """

    def __init__(self, **kwargs) -> None:
        """Initialize settings."""
        super().__init__(**kwargs)

        self._connect_mode = kwargs.get("connect_mode", HsmsConnectMode.ACTIVE)
        self._address = kwargs.get("address", "127.0.0.1")
        self._port = kwargs.get("port", 5000)

    @property
    def connect_mode(self) -> HsmsConnectMode:
        """Hsms connect mode.

        Default: HsmsConnectMode.ACTIVE
        """
        return self._connect_mode

    @property
    def address(self) -> str:
        """Remote (active) or local (passive) IP address.

        Default: "127.0.0.1"
        """
        return self._address

    @property
    def port(self) -> int:
        """TCP port of remote host.

        Default: 5000
        """
        return self._port

    def create_protocol(self) -> secsgem_cyg.common.Protocol:
        """Protocol class for this configuration."""
        from .protocol import HsmsProtocol  # pylint: disable=import-outside-toplevel

        return HsmsProtocol(self)

    def create_connection(self) -> secsgem_cyg.common.Connection:
        """Connection class for this configuration."""
        if self.connect_mode == HsmsConnectMode.ACTIVE:
            return secsgem_cyg.common.TcpClientConnection(self)
        return secsgem_cyg.common.TcpServerConnection(self)

    @property
    def name(self) -> str:
        """Name of this configuration."""
        return f"HSMS-{self.connect_mode}_{self.address}:{self.port}"

    @property
    def is_active(self) -> bool:
        """Check if connection is active."""
        return self.connect_mode == HsmsConnectMode.ACTIVE

    def generate_thread_name(self, functionality: str) -> str:
        """Generate a unique thread name for this configuration and a provided functionality.

        Args:
            functionality: name of the functionality to generate thread name for

        Returns:
            generated thread name

        """
        return f"secsgem_HSMS_{functionality}_{self.connect_mode}_{self.address}:{self.port}"


class ExistingProtocolSettings(HsmsSettings):
    """Settings for existing HSMS connection.

    These attributes can be initialized in the constructor and accessed as property.

    Example:
        >>> import secsgem_cyg.hsms
        >>>
        >>> settings = secsgem_cyg.hsms.HsmsSettings(device_type=secsgem_cyg.common.DeviceType.EQUIPMENT)
        >>> settings.device_type
        <DeviceType.EQUIPMENT: 0>

    """

    def __init__(self, **kwargs) -> None:
        """Initialize settings."""
        super().__init__(**kwargs)

        self._existing_protocol = kwargs.get("existing_protocol", None)

    @property
    def existing_protocol(self) -> secsgem_cyg.common.Protocol:
        """Existing protocol.

        Default: None
        """
        return self._existing_protocol

    def create_protocol(self) -> secsgem_cyg.common.Protocol:
        """Protocol class for this configuration."""
        return self.existing_protocol

    @property
    def name(self) -> str:
        """Name of this configuration."""
        return f"HSMS-{self.connect_mode}_{self.address}:{self.port}"
