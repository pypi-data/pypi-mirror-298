"""Wrapper for GEM collection event report."""
from __future__ import annotations

import secsgem_cyg.secs


class CollectionEventReport:  # pylint: disable=too-few-public-methods
    """Report definition for registered collection events."""

    def __init__(self,
                 rptid: int | str,
                 variables: list[int | str],
                 **kwargs):
        """Initialize a collection event report.

        You can manually set the secs-type of the id with the 'id_type' keyword argument.

        Args:
            rptid: ID of the report
            variables: long name of the collection event
            **kwargs: additional attributes for object

        """
        self.rptid = rptid
        self.vars = variables

        self.id_type: type[secsgem_cyg.secs.variables.Base]

        if isinstance(self.rptid, int):
            self.id_type = secsgem_cyg.secs.variables.U4
        else:
            self.id_type = secsgem_cyg.secs.variables.String

        for key, value in kwargs.items():
            setattr(self, key, value)
