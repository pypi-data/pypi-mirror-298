"""SHEAD data item."""
from .. import variables
from .base import DataItemBase


class SHEAD(DataItemBase):
    """SECS message header.

    :Type: :class:`Binary <secsgem_cyg.secs.variables.Binary>`
    :Length: 10

    **Used In Function**
        - :class:`SecsS09F09 <secsgem_cyg.secs.functions.SecsS09F09>`

    """

    __type__ = variables.Binary
    __count__ = 10
