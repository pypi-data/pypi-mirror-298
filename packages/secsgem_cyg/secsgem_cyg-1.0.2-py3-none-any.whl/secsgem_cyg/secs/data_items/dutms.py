"""DUTMS data item."""
from .. import variables
from .base import DataItemBase


class DUTMS(DataItemBase):
    """Die units of measure.

    :Type: :class:`String <secsgem_cyg.secs.variables.String>`

    **Used In Function**
        - :class:`SecsS12F01 <secsgem_cyg.secs.functions.SecsS12F01>`
        - :class:`SecsS12F04 <secsgem_cyg.secs.functions.SecsS12F04>`

    """

    __type__ = variables.String
