"""Forecasting model registry constants."""

DEFAULT_FORECAST_HORIZONS_HOURS = (1, 2, 3, 6, 12, 18, 24)
FORECAST_MODEL_FAMILIES = (
    "lstm",
    "cnn",
    "cnn_lstm",
    "attention_lstm",
    "arima",
    "persistence",
)
