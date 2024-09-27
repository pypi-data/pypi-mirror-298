"""PPGNT data item."""
from .. import variables
from .base import DataItemBase


class PPGNT(DataItemBase):
    """Process program grant status.

    :Type: :class:`Binary <secsgem_cyg.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+------------------------+--------------------------------------------------------+
        | Value | Description            | Constant                                               |
        +=======+========================+========================================================+
        | 0     | OK                     | :const:`secsgem_cyg.secs.data_items.PPGNT.OK`              |
        +-------+------------------------+--------------------------------------------------------+
        | 1     | Already have           | :const:`secsgem_cyg.secs.data_items.PPGNT.ALREADY_HAVE`    |
        +-------+------------------------+--------------------------------------------------------+
        | 2     | No space               | :const:`secsgem_cyg.secs.data_items.PPGNT.NO_SPACE`        |
        +-------+------------------------+--------------------------------------------------------+
        | 3     | Invalid PPID           | :const:`secsgem_cyg.secs.data_items.PPGNT.INVALID_PPID`    |
        +-------+------------------------+--------------------------------------------------------+
        | 4     | Busy, try later        | :const:`secsgem_cyg.secs.data_items.PPGNT.BUSY`            |
        +-------+------------------------+--------------------------------------------------------+
        | 5     | Will not accept        | :const:`secsgem_cyg.secs.data_items.PPGNT.WILL_NOT_ACCEPT` |
        +-------+------------------------+--------------------------------------------------------+
        | 6-63  | Reserved, other errors |                                                        |
        +-------+------------------------+--------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS07F02 <secsgem_cyg.secs.functions.SecsS07F02>`

    """

    __type__ = variables.Binary
    __count__ = 1

    OK = 0
    ALREADY_HAVE = 1
    NO_SPACE = 2
    INVALID_PPID = 3
    BUSY = 4
    WILL_NOT_ACCEPT = 5
