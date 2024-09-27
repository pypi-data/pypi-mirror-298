"""MID data item."""
from .. import variables
from .base import DataItemBase


class MID(DataItemBase):
    """Material ID.

    :Types:
       - :class:`String <secsgem_cyg.secs.variables.String>`
       - :class:`Binary <secsgem_cyg.secs.variables.Binary>`
    :Length: 80

    **Used In Function**
        - :class:`SecsS12F01 <secsgem_cyg.secs.functions.SecsS12F01>`
        - :class:`SecsS12F03 <secsgem_cyg.secs.functions.SecsS12F03>`
        - :class:`SecsS12F04 <secsgem_cyg.secs.functions.SecsS12F04>`
        - :class:`SecsS12F05 <secsgem_cyg.secs.functions.SecsS12F05>`
        - :class:`SecsS12F07 <secsgem_cyg.secs.functions.SecsS12F07>`
        - :class:`SecsS12F09 <secsgem_cyg.secs.functions.SecsS12F09>`
        - :class:`SecsS12F11 <secsgem_cyg.secs.functions.SecsS12F11>`
        - :class:`SecsS12F13 <secsgem_cyg.secs.functions.SecsS12F13>`
        - :class:`SecsS12F14 <secsgem_cyg.secs.functions.SecsS12F14>`
        - :class:`SecsS12F15 <secsgem_cyg.secs.functions.SecsS12F15>`
        - :class:`SecsS12F16 <secsgem_cyg.secs.functions.SecsS12F16>`
        - :class:`SecsS12F17 <secsgem_cyg.secs.functions.SecsS12F17>`
        - :class:`SecsS12F18 <secsgem_cyg.secs.functions.SecsS12F18>`

    """

    __type__ = variables.Dynamic
    __allowedtypes__ = [
        variables.String,
        variables.Binary
    ]
    __count__ = 80
