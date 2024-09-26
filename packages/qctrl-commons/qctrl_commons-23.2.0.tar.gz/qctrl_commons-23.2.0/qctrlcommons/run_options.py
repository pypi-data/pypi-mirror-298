"""Dataclasses defining options for Fire Opal circuit execution."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class RunOptions:
    """
    Provider-agnostic options for Fire Opal circuit execution.
    """


@dataclass
class IbmRunOptions(RunOptions):
    """
    Options for circuit execution on IBM devices through Fire Opal.

    Parameters
    ----------
    session_id: str or None, optional
        The ID of an IBM Runtime session to use for circuit execution.
        Defaults to None.
    """

    session_id: Optional[str] = None
