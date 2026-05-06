"""Forecast providers and wrappers that append predictions to observations."""

from dataclasses import dataclass
from typing import Protocol, Sequence

from energy_arbitrage_rl_cbf.forecasting.models import DEFAULT_FORECAST_HORIZONS_HOURS


class ForecastProvider(Protocol):
    def predict(self, horizon_hours: int, history: Sequence[float]) -> float:
        """Predict a future electricity price for one horizon."""


@dataclass(frozen=True)
class ForecastWrapperConfig:
    horizons_hours: tuple[int, ...] = DEFAULT_FORECAST_HORIZONS_HOURS


def append_forecasts(
    base_observation: Sequence[float],
    forecasts: Sequence[float],
) -> tuple[float, ...]:
    """Return an immutable observation with forecasts appended."""

    return (*base_observation, *forecasts)
