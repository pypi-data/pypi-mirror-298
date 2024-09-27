"""NULBC data item."""
from .. import variables
from .base import DataItemBase


class NULBC(DataItemBase):
    """Column count in dies.

    :Types:
       - :class:`U1 <secsgem_cyg.secs.variables.U1>`
       - :class:`String <secsgem_cyg.secs.variables.String>`

    **Used In Function**
        - :class:`SecsS12F01 <secsgem_cyg.secs.functions.SecsS12F01>`
        - :class:`SecsS12F03 <secsgem_cyg.secs.functions.SecsS12F03>`
        - :class:`SecsS12F04 <secsgem_cyg.secs.functions.SecsS12F04>`

    """

    __type__ = variables.Dynamic
    __allowedtypes__ = [
        variables.U1,
        variables.String
    ]
