"""Class for stream 07 function 04."""

from secsgem_cyg.secs.data_items import ACKC7
from secsgem_cyg.secs.functions.base import SecsStreamFunction


class SecsS07F04(SecsStreamFunction):
    """process program - acknowledge.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem_cyg.secs
        >>> secsgem_cyg.secs.functions.SecsS07F04
        ACKC7: B[1]

        >>> import secsgem_cyg.secs
        >>> secsgem_cyg.secs.functions.SecsS07F04(secsgem_cyg.secs.data_items.ACKC7.MATRIX_OVERFLOW)
        S7F4
          <B 0x3> .

    Data Items:
        - :class:`ACKC7 <secsgem.secs.data_items.ACKC7>`

    """

    _stream = 7
    _function = 4

    _data_format = ACKC7

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
