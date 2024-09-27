"""SDBIN data item."""
from .. import variables
from .base import DataItemBase


class SDBIN(DataItemBase):
    """Send bin information.

    :Type: :class:`Binary <secsgem_cyg.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+---------------------------+--------------------------------------------------+
        | Value | Description               | Constant                                         |
        +=======+===========================+==================================================+
        | 0     | Send bin information      | :const:`secsgem_cyg.secs.data_items.SDBIN.SEND`      |
        +-------+---------------------------+--------------------------------------------------+
        | 1     | Don't send bin infomation | :const:`secsgem_cyg.secs.data_items.SDBIN.DONT_SEND` |
        +-------+---------------------------+--------------------------------------------------+
        | 2-63  | Reserved                  |                                                  |
        +-------+---------------------------+--------------------------------------------------+

    **Used In Function**
        - :class:`SecsS12F17 <secsgem_cyg.secs.functions.SecsS12F17>`

    """

    __type__ = variables.Binary
    __count__ = 1

    SEND = 0
    DONT_SEND = 1
