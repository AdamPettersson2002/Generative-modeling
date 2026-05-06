"""Battery model primitives shared by the environment and safety filters."""

from dataclasses import dataclass


@dataclass(frozen=True)
class BatteryConfig:
    """Battery parameters following the paper's sign convention."""

    capacity_mwh: float = 10.0
    min_soc: float = 0.2
    max_soc: float = 0.8
    charge_limit_mw: float = -2.5
    discharge_limit_mw: float = 2.5
    charge_efficiency: float = 0.92
    discharge_efficiency: float = 1.0
    self_discharge: float = 0.0
    peukert_constant: float = 1.14
    cycles_to_failure: float = 6000.0
    investment_cost_per_mwh: float = 300_000.0
    timestep_hours: float = 1.0

    def validate(self) -> None:
        if self.capacity_mwh <= 0:
            raise ValueError("capacity_mwh must be positive")
        if not 0 <= self.min_soc < self.max_soc <= 1:
            raise ValueError("SOC bounds must satisfy 0 <= min_soc < max_soc <= 1")
        if self.charge_limit_mw >= 0:
            raise ValueError("charge_limit_mw should be negative")
        if self.discharge_limit_mw <= 0:
            raise ValueError("discharge_limit_mw should be positive")
        if self.charge_efficiency <= 0 or self.discharge_efficiency <= 0:
            raise ValueError("efficiencies must be positive")
        if self.timestep_hours <= 0:
            raise ValueError("timestep_hours must be positive")


def feasible_action_bounds(soc: float, config: BatteryConfig) -> tuple[float, float]:
    """Return action bounds that keep next-step SOC inside limits.

    Positive actions discharge the battery. Negative actions charge it.
    """

    config.validate()
    effective_soc = soc * (1.0 - config.self_discharge)
    discharge_headroom = max(0.0, effective_soc - config.min_soc)
    charge_headroom = max(0.0, config.max_soc - effective_soc)

    soc_limited_discharge = (
        discharge_headroom
        * config.capacity_mwh
        * config.discharge_efficiency
        / config.timestep_hours
    )
    soc_limited_charge = (
        charge_headroom
        * config.capacity_mwh
        / (config.charge_efficiency * config.timestep_hours)
    )

    lower = max(config.charge_limit_mw, -soc_limited_charge)
    upper = min(config.discharge_limit_mw, soc_limited_discharge)
    return lower, upper


def clip_action_to_soc_bounds(action_mw: float, soc: float, config: BatteryConfig) -> float:
    """Clip an action to power limits and one-step SOC feasibility."""

    lower, upper = feasible_action_bounds(soc=soc, config=config)
    return min(max(action_mw, lower), upper)


def next_soc(soc: float, action_mw: float, config: BatteryConfig) -> float:
    """Compute next SOC after applying a feasible action for one time step."""

    action_mw = clip_action_to_soc_bounds(action_mw=action_mw, soc=soc, config=config)
    soc_after_self_discharge = soc * (1.0 - config.self_discharge)

    if action_mw >= 0:
        delta_soc = -(action_mw * config.timestep_hours) / (
            config.discharge_efficiency * config.capacity_mwh
        )
    else:
        delta_soc = (-action_mw * config.charge_efficiency * config.timestep_hours) / (
            config.capacity_mwh
        )

    return min(max(soc_after_self_discharge + delta_soc, config.min_soc), config.max_soc)
