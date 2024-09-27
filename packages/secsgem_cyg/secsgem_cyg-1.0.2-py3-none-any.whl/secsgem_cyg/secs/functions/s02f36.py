"""Class for stream 02 function 36."""

from secsgem_cyg.secs.data_items import LRACK
from secsgem_cyg.secs.functions.base import SecsStreamFunction


class SecsS02F36(SecsStreamFunction):
    """link event report - acknowledge.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem_cyg.secs
        >>> secsgem_cyg.secs.functions.SecsS02F36
        LRACK: B[1]

        >>> import secsgem_cyg.secs
        >>> secsgem_cyg.secs.functions.SecsS02F36(secsgem_cyg.secs.data_items.LRACK.CEID_UNKNOWN)
        S2F36
          <B 0x4> .

    Data Items:
        - :class:`LRACK <secsgem.secs.data_items.LRACK>`

    """

    _stream = 2
    _function = 36

    _data_format = LRACK

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
