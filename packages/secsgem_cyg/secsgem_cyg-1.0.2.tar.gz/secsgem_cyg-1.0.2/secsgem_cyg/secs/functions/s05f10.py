"""Class for stream 05 function 10."""

from secsgem_cyg.secs.functions.base import SecsStreamFunction


class SecsS05F10(SecsStreamFunction):
    """exception post - confirm.

    Examples:
        >>> import secsgem_cyg.secs
        >>> secsgem_cyg.secs.functions.SecsS05F10
        Header only

        >>> import secsgem_cyg.secs
        >>> secsgem_cyg.secs.functions.SecsS05F10()
        S5F10 .

    """

    _stream = 5
    _function = 10

    _data_format = None

    _to_host = False
    _to_equipment = True

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = False
