"""Control barrier function safety filter for battery actions."""

from dataclasses import dataclass

from energy_arbitrage_rl_cbf.envs.battery_model import (
    BatteryConfig,
    clip_action_to_soc_bounds,
    feasible_action_bounds,
)


@dataclass(frozen=True)
class CbfFilterConfig:
    """CBF projection settings.

    For one-dimensional SOC safety, the CBF projection is equivalent to clipping
    the nominal action into the feasible one-step action interval. This file is
    the future home for a QP-backed implementation when more constraints are
    introduced.
    """

    alpha: float = 1.0
    projection: str = "closed_form_1d"


class CbfSafetyFilter:
    """Filter an SB3 policy action before it reaches the battery environment."""

    def __init__(
        self,
        battery_config: BatteryConfig | None = None,
        filter_config: CbfFilterConfig | None = None,
    ) -> None:
        self.battery_config = battery_config or BatteryConfig()
        self.filter_config = filter_config or CbfFilterConfig()

    def feasible_interval(self, soc: float) -> tuple[float, float]:
        return feasible_action_bounds(soc=soc, config=self.battery_config)

    def filter(self, nominal_action_mw: float, soc: float) -> float:
        return clip_action_to_soc_bounds(
            action_mw=nominal_action_mw,
            soc=soc,
            config=self.battery_config,
        )
