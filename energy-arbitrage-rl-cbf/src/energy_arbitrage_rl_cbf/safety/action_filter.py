"""Common action-filter protocol."""

from typing import Protocol


class ActionFilter(Protocol):
    def filter(self, nominal_action_mw: float, soc: float) -> float:
        """Return the action that should be passed to the environment."""


class NoOpActionFilter:
    def filter(self, nominal_action_mw: float, soc: float) -> float:
        return nominal_action_mw
