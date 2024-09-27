"""Class for stream 02 function 34."""

from secsgem_cyg.secs.data_items import DRACK
from secsgem_cyg.secs.functions.base import SecsStreamFunction


class SecsS02F34(SecsStreamFunction):
    """define report - acknowledge.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem_cyg.secs
        >>> secsgem_cyg.secs.functions.SecsS02F34
        DRACK: B[1]

        >>> import secsgem_cyg.secs
        >>> secsgem_cyg.secs.functions.SecsS02F34(secsgem_cyg.secs.data_items.DRACK.INVALID_FORMAT)
        S2F34
          <B 0x2> .

    Data Items:
        - :class:`DRACK <secsgem.secs.data_items.DRACK>`

    """

    _stream = 2
    _function = 34

    _data_format = DRACK

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
