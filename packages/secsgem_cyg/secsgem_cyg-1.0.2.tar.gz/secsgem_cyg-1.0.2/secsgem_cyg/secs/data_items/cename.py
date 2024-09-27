"""CENAME data item."""
from .. import variables
from .base import DataItemBase


class CENAME(DataItemBase):
    """Collection event Name.

    :Type: :class:`String <secsgem_cyg.secs.variables.String>`

    **Used In Function**
        - :class:`SecsS01F24 <secsgem_cyg.secs.functions.SecsS01F24>`

    """

    __type__ = variables.String
