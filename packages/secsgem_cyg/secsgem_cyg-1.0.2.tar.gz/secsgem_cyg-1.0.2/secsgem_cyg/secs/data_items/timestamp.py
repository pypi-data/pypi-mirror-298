"""TIMESTAMP data item."""
from .. import variables
from .base import DataItemBase


class TIMESTAMP(DataItemBase):
    """Timestamp.

    :Type: :class:`String <secsgem_cyg.secs.variables.String>`
    :Length: 32

    **Used In Function**
        - :class:`SecsS05F09 <secsgem_cyg.secs.functions.SecsS05F09>`
        - :class:`SecsS05F11 <secsgem_cyg.secs.functions.SecsS05F11>`
        - :class:`SecsS05F15 <secsgem_cyg.secs.functions.SecsS05F15>`

    """

    __type__ = variables.String
    __count__ = 32
