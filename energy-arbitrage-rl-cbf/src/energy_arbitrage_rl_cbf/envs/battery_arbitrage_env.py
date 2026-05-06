"""Gymnasium environment scaffold for battery energy arbitrage."""

from dataclasses import dataclass

from energy_arbitrage_rl_cbf.envs.battery_model import BatteryConfig


@dataclass(frozen=True)
class EnvironmentConfig:
    """Environment settings that should mirror the YAML config."""

    battery: BatteryConfig = BatteryConfig()
    forecast_horizons_hours: tuple[int, ...] = ()
    episode_length_hours: int = 8760
    include_degradation_cost: bool = True


class BatteryArbitrageEnv:
    """Placeholder for the Gymnasium environment used by SB3.

    Planned observation:
    - basic: [soc, current_price]
    - forecasted: [soc, current_price, forecast_1h, ..., forecast_24h]

    Planned action:
    - scalar battery power in MW, positive for discharge and negative for charge
    """

    def __init__(self, config: EnvironmentConfig) -> None:
        self.config = config

    def reset(self) -> None:
        raise NotImplementedError("Wire this to processed hourly data and Gymnasium spaces.")

    def step(self, action_mw: float) -> None:
        raise NotImplementedError("Implement reward, transition, and terminated/truncated flags.")
