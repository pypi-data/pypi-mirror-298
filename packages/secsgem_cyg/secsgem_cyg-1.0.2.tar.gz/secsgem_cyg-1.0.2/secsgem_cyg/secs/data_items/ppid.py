"""PPID data item."""
from .. import variables
from .base import DataItemBase


class PPID(DataItemBase):
    """Process program ID.

    :Types:
       - :class:`String <secsgem_cyg.secs.variables.String>`
       - :class:`Binary <secsgem_cyg.secs.variables.Binary>`
    :Length: 120

    **Used In Function**
        - :class:`SecsS07F01 <secsgem_cyg.secs.functions.SecsS07F01>`
        - :class:`SecsS07F03 <secsgem_cyg.secs.functions.SecsS07F03>`
        - :class:`SecsS07F05 <secsgem_cyg.secs.functions.SecsS07F05>`
        - :class:`SecsS07F06 <secsgem_cyg.secs.functions.SecsS07F06>`
        - :class:`SecsS07F17 <secsgem_cyg.secs.functions.SecsS07F17>`
        - :class:`SecsS07F20 <secsgem_cyg.secs.functions.SecsS07F20>`

    """

    __type__ = variables.Dynamic
    __allowedtypes__ = [
        variables.String,
        variables.Binary
    ]
    __count__ = 120
