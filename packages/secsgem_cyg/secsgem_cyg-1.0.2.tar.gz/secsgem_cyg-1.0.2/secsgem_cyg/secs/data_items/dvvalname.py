"""DVVALNAME data item."""
from .. import variables
from .base import DataItemBase


class DVVALNAME(DataItemBase):
    """Data value name.

    :Type: :class:`String <secsgem_cyg.secs.variables.String>`

    **Used In Function**
        - :class:`SecsS01F22 <secsgem_cyg.secs.functions.SecsS01F22>`

    """

    __type__ = variables.String
