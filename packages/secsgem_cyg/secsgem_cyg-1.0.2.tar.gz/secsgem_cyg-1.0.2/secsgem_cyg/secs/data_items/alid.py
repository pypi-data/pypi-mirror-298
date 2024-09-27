"""ALID data item."""
from .. import variables
from .base import DataItemBase


class ALID(DataItemBase):
    """Alarm ID.

    :Types:
       - :class:`U1 <secsgem_cyg.secs.variables.U1>`
       - :class:`U2 <secsgem_cyg.secs.variables.U2>`
       - :class:`U4 <secsgem_cyg.secs.variables.U4>`
       - :class:`U8 <secsgem_cyg.secs.variables.U8>`
       - :class:`I1 <secsgem_cyg.secs.variables.I1>`
       - :class:`I2 <secsgem_cyg.secs.variables.I2>`
       - :class:`I4 <secsgem_cyg.secs.variables.I4>`
       - :class:`I8 <secsgem_cyg.secs.variables.I8>`

    **Used In Function**
        - :class:`SecsS05F01 <secsgem_cyg.secs.functions.SecsS05F01>`
        - :class:`SecsS05F03 <secsgem_cyg.secs.functions.SecsS05F03>`
        - :class:`SecsS05F05 <secsgem_cyg.secs.functions.SecsS05F05>`
        - :class:`SecsS05F06 <secsgem_cyg.secs.functions.SecsS05F06>`
        - :class:`SecsS05F08 <secsgem_cyg.secs.functions.SecsS05F08>`

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
        variables.I8
    ]
