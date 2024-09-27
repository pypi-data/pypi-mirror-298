"""Class for stream 14 function 00."""

from secsgem_cyg.secs.functions.base import SecsStreamFunction


class SecsS14F00(SecsStreamFunction):
    """abort transaction stream 14.

    Examples:
        >>> import secsgem_cyg.secs
        >>> secsgem_cyg.secs.functions.SecsS14F00
        Header only

        >>> import secsgem_cyg.secs
        >>> secsgem_cyg.secs.functions.SecsS14F00()
        S14F0 .

    """

    _stream = 14
    _function = 0

    _data_format = None

    _to_host = True
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
