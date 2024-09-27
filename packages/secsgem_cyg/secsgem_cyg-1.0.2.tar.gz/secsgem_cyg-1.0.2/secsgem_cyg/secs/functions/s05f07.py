"""Class for stream 05 function 07."""

from secsgem_cyg.secs.functions.base import SecsStreamFunction


class SecsS05F07(SecsStreamFunction):
    """list enabled alarms - request.

    Examples:
        >>> import secsgem_cyg.secs
        >>> secsgem_cyg.secs.functions.SecsS05F07
        Header only

        >>> import secsgem_cyg.secs
        >>> secsgem_cyg.secs.functions.SecsS05F07()
        S5F7 W .

    """

    _stream = 5
    _function = 7

    _data_format = None

    _to_host = False
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
