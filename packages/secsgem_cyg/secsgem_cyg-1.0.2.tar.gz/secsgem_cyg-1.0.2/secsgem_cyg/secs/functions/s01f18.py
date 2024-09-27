"""Class for stream 01 function 18."""

from secsgem_cyg.secs.data_items import ONLACK
from secsgem_cyg.secs.functions.base import SecsStreamFunction


class SecsS01F18(SecsStreamFunction):
    """online acknowledge.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem_cyg.secs
        >>> secsgem_cyg.secs.functions.SecsS01F18
        ONLACK: B[1]

        >>> import secsgem_cyg.secs
        >>> secsgem_cyg.secs.functions.SecsS01F18(secsgem_cyg.secs.data_items.ONLACK.ALREADY_ON)
        S1F18
          <B 0x2> .

    Data Items:
        - :class:`ONLACK <secsgem.secs.data_items.ONLACK>`

    """

    _stream = 1
    _function = 18

    _data_format = ONLACK

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
