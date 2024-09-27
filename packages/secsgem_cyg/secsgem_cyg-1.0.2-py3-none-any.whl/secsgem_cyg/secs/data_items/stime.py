"""STIME data item."""
from .. import variables
from .base import DataItemBase


class STIME(DataItemBase):
    """Sample time.

    :Type: :class:`String <secsgem_cyg.secs.variables.String>`

    **Used In Function**
        - :class:`SecsS06F01 <secsgem_cyg.secs.functions.SecsS06F01>`

    """

    __type__ = variables.String
