"""STRP data item."""
from .. import variables
from .base import DataItemBase


class STRP(DataItemBase):
    """Starting position.

    :Types:
       - :class:`I1 <secsgem_cyg.secs.variables.I1>`
       - :class:`I2 <secsgem_cyg.secs.variables.I2>`
       - :class:`I4 <secsgem_cyg.secs.variables.I4>`
       - :class:`I8 <secsgem_cyg.secs.variables.I8>`
    :Length: 2

    **Used In Function**
        - :class:`SecsS12F09 <secsgem_cyg.secs.functions.SecsS12F09>`
        - :class:`SecsS12F16 <secsgem_cyg.secs.functions.SecsS12F16>`

    """

    __type__ = variables.Dynamic
    __allowedtypes__ = [
        variables.I1,
        variables.I2,
        variables.I4,
        variables.I8
    ]
    __count__ = 2
