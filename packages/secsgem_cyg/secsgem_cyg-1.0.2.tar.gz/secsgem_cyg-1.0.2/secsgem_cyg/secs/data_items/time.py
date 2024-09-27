"""TIME data item."""
from .. import variables
from .base import DataItemBase


class TIME(DataItemBase):
    """Time of day.

    :Type: :class:`String <secsgem_cyg.secs.variables.String>`
    :Length: 32

    **Used In Function**
        - :class:`SecsS02F18 <secsgem_cyg.secs.functions.SecsS02F18>`

    """

    __type__ = variables.String
    __count__ = 32
