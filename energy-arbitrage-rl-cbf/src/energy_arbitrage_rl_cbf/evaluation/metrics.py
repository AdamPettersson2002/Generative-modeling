"""Metric helpers for paper reproduction and CBF comparisons."""

from dataclasses import dataclass


@dataclass(frozen=True)
class EpisodeMetrics:
    accumulated_reward: float
    grid_revenue: float
    degradation_cost: float
    charge_discharge_events: int
    soc_violations: int = 0
    nominal_action_adjustment: float = 0.0


def improvement_percent(candidate: float, baseline: float) -> float:
    if baseline == 0:
        raise ValueError("baseline must be non-zero")
    return 100.0 * (candidate - baseline) / abs(baseline)
