"""Class for stream 05 function 12."""

from secsgem_cyg.secs.functions.base import SecsStreamFunction


class SecsS05F12(SecsStreamFunction):
    """exception clear - confirm.

    Examples:
        >>> import secsgem_cyg.secs
        >>> secsgem_cyg.secs.functions.SecsS05F12
        Header only

        >>> import secsgem_cyg.secs
        >>> secsgem_cyg.secs.functions.SecsS05F12()
        S5F12 .

    """

    _stream = 5
    _function = 12

    _data_format = None

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
