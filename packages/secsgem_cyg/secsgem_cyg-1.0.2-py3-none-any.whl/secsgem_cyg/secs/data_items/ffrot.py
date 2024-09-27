"""FFROT data item."""
from .. import variables
from .base import DataItemBase


class FFROT(DataItemBase):
    """Film frame rotation.

    In degrees from the bottom CW. (Bottom equals zero degrees.) Zero length indicates not used.

    :Type: :class:`U2 <secsgem_cyg.secs.variables.U2>`

    **Used In Function**
        - :class:`SecsS12F01 <secsgem_cyg.secs.functions.SecsS12F01>`
        - :class:`SecsS12F03 <secsgem_cyg.secs.functions.SecsS12F03>`

    """

    __type__ = variables.U2
