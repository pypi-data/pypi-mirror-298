"""VID data item."""
from .. import variables
from .base import DataItemBase


class VID(DataItemBase):
    """Variable ID.

    :Types:
       - :class:`U1 <secsgem_cyg.secs.variables.U1>`
       - :class:`U2 <secsgem_cyg.secs.variables.U2>`
       - :class:`U4 <secsgem_cyg.secs.variables.U4>`
       - :class:`U8 <secsgem_cyg.secs.variables.U8>`
       - :class:`I1 <secsgem_cyg.secs.variables.I1>`
       - :class:`I2 <secsgem_cyg.secs.variables.I2>`
       - :class:`I4 <secsgem_cyg.secs.variables.I4>`
       - :class:`I8 <secsgem_cyg.secs.variables.I8>`
       - :class:`String <secsgem_cyg.secs.variables.String>`

    **Used In Function**
        - :class:`SecsS01F21 <secsgem_cyg.secs.functions.SecsS01F21>`
        - :class:`SecsS01F22 <secsgem_cyg.secs.functions.SecsS01F22>`
        - :class:`SecsS01F24 <secsgem_cyg.secs.functions.SecsS01F24>`
        - :class:`SecsS02F33 <secsgem_cyg.secs.functions.SecsS02F33>`
        - :class:`SecsS02F45 <secsgem_cyg.secs.functions.SecsS02F45>`
        - :class:`SecsS02F46 <secsgem_cyg.secs.functions.SecsS02F46>`
        - :class:`SecsS02F47 <secsgem_cyg.secs.functions.SecsS02F47>`
        - :class:`SecsS02F48 <secsgem_cyg.secs.functions.SecsS02F48>`
        - :class:`SecsS06F22 <secsgem_cyg.secs.functions.SecsS06F22>`

    """

    __type__ = variables.Dynamic
    __allowedtypes__ = [
        variables.U1,
        variables.U2,
        variables.U4,
        variables.U8,
        variables.I1,
        variables.I2,
        variables.I4,
        variables.I8,
        variables.String
    ]
