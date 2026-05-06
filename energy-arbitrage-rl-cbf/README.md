# Energy Arbitrage RL + CBF

Replication and extension workspace for:

**"Enhancing Battery Storage Energy Arbitrage with Deep Reinforcement Learning and Time-Series Forecasting"** by Sage, Campbell, and Zhao.

The first milestone is a faithful reproduction of the paper's battery energy arbitrage experiments. The second milestone is a safety-oriented extension where a Stable-Baselines3 policy acts as the nominal controller and a control barrier function (CBF) safety filter modifies unsafe actions before they reach the environment.

## Project Shape

```text
energy-arbitrage-rl-cbf/
  configs/
    replication/        # Paper reproduction configs
    cbf/                # CBF extension configs
  data/
    raw/                # Original AESO, ERA5, or paper dataset files
    processed/          # Cleaned hourly time series and train/val/test splits
    external/           # Any downloaded reference data kept out of src
  docs/
    paper_notes.md      # Replication notes extracted from the article
  notebooks/            # Exploration and result inspection
  outputs/
    checkpoints/        # SB3 agents and forecaster weights
    figures/            # Paper reproduction plots
    metrics/            # CSV/JSON evaluation summaries
  scripts/              # Command-line entry points
  src/
    energy_arbitrage_rl_cbf/
      agents/           # SB3 training/evaluation orchestration
      data/             # Dataset loading and sliding-window builders
      envs/             # Battery arbitrage model and Gymnasium env
      evaluation/       # Reward, revenue, safety, and paper metric helpers
      forecasting/      # Time-series predictors and forecast wrappers
      safety/           # Action filters and CBF safety layer
      utils/            # Config and path helpers
  tests/                # Unit tests for env dynamics, filters, and metrics
```

## Implementation Phases

1. Rebuild the paper environment:
   - battery state of charge (SOC), hourly electricity price, and optional forecast observations
   - one-dimensional battery power action, with positive values for discharge and negative values for charge
   - reward as grid revenue minus degradation cost
   - paper-style hard safety layer for SOC and charge/discharge limits

2. Reproduce the forecasting setup:
   - hourly Alberta price data, plus optional demand/weather/time features
   - horizons of 1h, 2h, 3h, 6h, 12h, 18h, and 24h
   - LSTM, CNN, CNN-LSTM, attention-LSTM, ARIMA, and persistence baselines

3. Reproduce RL results:
   - DQN and PPO with Stable-Baselines3
   - no-forecast, perfect-forecast, and predicted-forecast experiments
   - compare accumulated reward, charging activity, forecast error, and runtime

4. Add the CBF extension:
   - keep the trained SB3 agent as the nominal policy
   - pass proposed actions through `safety.CbfSafetyFilter`
   - begin with closed-form one-dimensional SOC safety projection
   - upgrade to a QP-based filter when adding richer constraints such as degradation, ramping, reserve margins, or grid limits

## First Coding Targets

Start with these files:

1. `src/energy_arbitrage_rl_cbf/envs/battery_model.py`
2. `src/energy_arbitrage_rl_cbf/envs/battery_arbitrage_env.py`
3. `src/energy_arbitrage_rl_cbf/safety/cbf_filter.py`
4. `scripts/train_agent.py`
5. `configs/replication/base.yaml`

Raw datasets, generated checkpoints, and result files should stay out of git unless they are intentionally small examples.
