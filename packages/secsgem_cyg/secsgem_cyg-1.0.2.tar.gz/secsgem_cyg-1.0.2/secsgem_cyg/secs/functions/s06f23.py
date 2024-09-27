"""Class for stream 06 function 23."""

from secsgem_cyg.secs.data_items import RSDC
from secsgem_cyg.secs.functions.base import SecsStreamFunction


class SecsS06F23(SecsStreamFunction):
    """Request spooled data.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem_cyg.secs
        >>> secsgem_cyg.secs.functions.SecsS06F23
        RSDC: U1[1]

        >>> import secsgem_cyg.secs
        >>> secsgem_cyg.secs.functions.SecsS06F23(secsgem_cyg.secs.data_items.RSDC.PURGE)
        S6F23 W
          <U1 1 > .

    Data Items:
        - :class:`RSDC <secsgem.secs.data_items.RSDC>`

    """

    _stream = 6
    _function = 23

    _data_format = RSDC

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
