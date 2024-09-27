"""TIAACK data item."""
from .. import variables
from .base import DataItemBase


class TIAACK(DataItemBase):
    """Equipment acknowledgement code.

    :Type: :class:`Binary <secsgem_cyg.secs.variables.Binary>`
    :Length: 1

    **Values**
        +-------+------------------------+--------------------------------------------------------+
        | Value | Description            | Constant                                               |
        +=======+========================+========================================================+
        | 0     | Everything correct     | :const:`secsgem_cyg.secs.data_items.TIAACK.OK`             |
        +-------+------------------------+--------------------------------------------------------+
        | 1     | Too many SVIDs         | :const:`secsgem_cyg.secs.data_items.TIAACK.SVID_EXCEEDED`  |
        +-------+------------------------+--------------------------------------------------------+
        | 2     | No more traces allowed | :const:`secsgem_cyg.secs.data_items.TIAACK.TRACES_DENIED`  |
        +-------+------------------------+--------------------------------------------------------+
        | 3     | Invalid period         | :const:`secsgem_cyg.secs.data_items.TIAACK.INVALID_PERIOD` |
        +-------+------------------------+--------------------------------------------------------+
        | 4     | Unknown SVID           | :const:`secsgem_cyg.secs.data_items.TIAACK.SVID_UNKNOWN`   |
        +-------+------------------------+--------------------------------------------------------+
        | 5     | Invalid REPGSZ         | :const:`secsgem_cyg.secs.data_items.TIAACK.REPGSZ_INVALID` |
        +-------+------------------------+--------------------------------------------------------+
        | 6-63  | Reserved               |                                                        |
        +-------+------------------------+--------------------------------------------------------+

    **Used In Function**
        - :class:`SecsS02F24 <secsgem_cyg.secs.functions.SecsS02F24>`

    """

    __type__ = variables.Binary
    __count__ = 1

    OK = 0
    SVID_EXCEEDED = 1
    TRACES_DENIED = 2
    INVALID_PERIOD = 3
    SVID_UNKNOWN = 4
    REPGSZ_INVALID = 5
