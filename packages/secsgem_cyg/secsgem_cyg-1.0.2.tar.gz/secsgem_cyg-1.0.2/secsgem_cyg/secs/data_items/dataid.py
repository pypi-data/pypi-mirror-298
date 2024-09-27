"""DATAID data item."""
from .. import variables
from .base import DataItemBase


class DATAID(DataItemBase):
    """Data ID.

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
        - :class:`SecsS02F33 <secsgem_cyg.secs.functions.SecsS02F33>`
        - :class:`SecsS02F35 <secsgem_cyg.secs.functions.SecsS02F35>`
        - :class:`SecsS02F45 <secsgem_cyg.secs.functions.SecsS02F45>`
        - :class:`SecsS02F49 <secsgem_cyg.secs.functions.SecsS02F49>`
        - :class:`SecsS06F05 <secsgem_cyg.secs.functions.SecsS06F05>`
        - :class:`SecsS06F07 <secsgem_cyg.secs.functions.SecsS06F07>`
        - :class:`SecsS06F08 <secsgem_cyg.secs.functions.SecsS06F08>`
        - :class:`SecsS06F11 <secsgem_cyg.secs.functions.SecsS06F11>`
        - :class:`SecsS06F16 <secsgem_cyg.secs.functions.SecsS06F16>`

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
