"""LIMITID data item."""
from .. import variables
from .base import DataItemBase


class LIMITID(DataItemBase):
    """Limit ID.

    :Type: :class:`Binary <secsgem_cyg.secs.variables.Binary>`
    :Length: 1

    **Used In Function**
        - :class:`SecsS02F45 <secsgem_cyg.secs.functions.SecsS02F45>`
        - :class:`SecsS02F46 <secsgem_cyg.secs.functions.SecsS02F46>`
        - :class:`SecsS02F48 <secsgem_cyg.secs.functions.SecsS02F48>`

    """

    __type__ = variables.Binary
    __count__ = 1
