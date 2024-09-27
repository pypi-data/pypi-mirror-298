"""MEXP data item."""
from .. import variables
from .base import DataItemBase


class MEXP(DataItemBase):
    """Message expected.

    :Type: :class:`String <secsgem_cyg.secs.variables.String>`
    :Length: 6

    **Used In Function**
        - :class:`SecsS09F13 <secsgem_cyg.secs.functions.SecsS09F13>`

    """

    __type__ = variables.String
    __count__ = 6
