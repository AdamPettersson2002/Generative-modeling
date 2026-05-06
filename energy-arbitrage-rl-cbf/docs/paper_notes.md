# Paper Notes

Source PDF: `EnergyArbitrageRLTSA.pdf`

Paper title: "Enhancing Battery Storage Energy Arbitrage with Deep Reinforcement Learning and Time-Series Forecasting".

## Replication Targets

- Case study: grid-connected battery energy storage in Alberta, Canada.
- Data: hourly electricity market data and weather/climate data for 2018-2022.
- Basic RL state: battery SOC and current electricity price.
- Forecast RL state: SOC, current electricity price, and predicted prices for future horizons.
- Forecast horizons: 1h, 2h, 3h, 6h, 12h, 18h, and 24h.
- Action: one-dimensional battery power. Positive action discharges the battery, negative action charges it.
- Reward: grid revenue minus battery degradation cost.
- Safety baseline: hard action correction to keep SOC and charge/discharge power inside limits.
- Main RL algorithms: DQN and PPO via Gymnasium and Stable-Baselines3.
- Forecasting models: LSTM, CNN, CNN-LSTM, attention-LSTM, ARIMA, and persistence baselines.
- Tuning stack in the paper: PyTorch for forecasters, Stable-Baselines3 for RL, Optuna for tuning.

## Battery Parameters From The Paper

| Parameter | Value |
| --- | --- |
| Capacity | 10 MWh |
| SOC bounds | 0.2 to 0.8 |
| Charge/discharge limits | -2.5 MW to 2.5 MW |
| Charge efficiency | 0.92 |
| Discharge efficiency | 1.0 |
| Self-discharge | 0 |
| Peukert constant | 1.14 |
| Cycles to failure | 6000 |
| Investment cost | 300000 per MWh |

## CBF Extension Idea

The paper already has a hard safety layer that clips unsafe battery actions. The extension should make this explicit as a safety filter:

1. Let the SB3 policy produce a nominal action.
2. Treat SOC limits as barrier constraints.
3. Project the nominal action onto the feasible action set before stepping the environment.
4. Log both the nominal action and filtered action so reward changes can be separated from safety interventions.

For the first CBF prototype, SOC safety is one-dimensional and can be solved as a closed-form projection. If the safety model later includes richer constraints, move the projection into a small quadratic program.
