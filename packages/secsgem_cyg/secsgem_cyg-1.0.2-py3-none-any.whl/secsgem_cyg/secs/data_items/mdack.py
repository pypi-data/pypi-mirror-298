"""MDACK data item."""
from .. import variables
from .base import DataItemBase


class MDACK(DataItemBase):
    """Map data acknowledge.

    :Type: :class:`Binary <secsgem_cyg.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+-------------------+-----------------------------------------------------+
        | Value | Description       | Constant                                            |
        +=======+===================+=====================================================+
        | 0     | Map received      | :const:`secsgem_cyg.secs.data_items.MDACK.ACK`          |
        +-------+-------------------+-----------------------------------------------------+
        | 1     | Format error      | :const:`secsgem_cyg.secs.data_items.MDACK.FORMAT_ERROR` |
        +-------+-------------------+-----------------------------------------------------+
        | 2     | No ID match       | :const:`secsgem_cyg.secs.data_items.MDACK.UNKNOWN_ID`   |
        +-------+-------------------+-----------------------------------------------------+
        | 3     | Abort/discard map | :const:`secsgem_cyg.secs.data_items.MDACK.ABORT_MAP`    |
        +-------+-------------------+-----------------------------------------------------+
        | 4-63  | Reserved, error   |                                                     |
        +-------+-------------------+-----------------------------------------------------+

    **Used In Function**
        - :class:`SecsS12F08 <secsgem_cyg.secs.functions.SecsS12F08>`
        - :class:`SecsS12F10 <secsgem_cyg.secs.functions.SecsS12F10>`
        - :class:`SecsS12F12 <secsgem_cyg.secs.functions.SecsS12F12>`

    """

    __type__ = variables.Binary
    __count__ = 1

    ACK = 0
    FORMAT_ERROR = 1
    UNKNOWN_ID = 2
    ABORT_MAP = 3
