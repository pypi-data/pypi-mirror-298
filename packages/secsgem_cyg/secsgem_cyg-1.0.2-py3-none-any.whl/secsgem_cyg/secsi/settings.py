"""SECS-I settings class."""
from __future__ import annotations

import secsgem_cyg.common


class SecsISettings(secsgem_cyg.common.Settings):
    """Settings for SECS-I connection.

    These attributes can be initialized in the constructor and accessed as property.

    Example:
        >>> import secsgem_cyg.secsi
        >>>
        >>> settings = secsgem_cyg.secsi.SecsISettings(port="COM1")
        >>> settings.port
        'COM1'
        >>> settings.speed
        9600

    """

    def __init__(self, **kwargs) -> None:
        """Initialize settings."""
        super().__init__(**kwargs)

        self._port = kwargs.get("port", "")
        self._speed = kwargs.get("speed", 9600)

    @property
    def port(self) -> str:
        """Serial port.

        Default: ""
        """
        return self._port

    @property
    def speed(self) -> int:
        """Serial port baud rate.

        Default: 9600
        """
        return self._speed

    def create_protocol(self) -> secsgem_cyg.common.Protocol:
        """Protocol class for this configuration."""
        from .protocol import SecsIProtocol  # pylint: disable=import-outside-toplevel

        return SecsIProtocol(self)

    def create_connection(self) -> secsgem_cyg.common.Connection:
        """Connection class for this configuration."""
        return secsgem_cyg.common.SerialConnection(self)

    @property
    def name(self) -> str:
        """Name of this configuration."""
        return f"SECSI-{self.port}"

    def generate_thread_name(self, functionality: str) -> str:
        """Generate a unique thread name for this configuration and a provided functionality.

        Args:
            functionality: name of the functionality to generate thread name for

        Returns:
            generated thread name

        """
        return f"secsgem_SecsI_{functionality}_{self.port}@{self.speed}"
