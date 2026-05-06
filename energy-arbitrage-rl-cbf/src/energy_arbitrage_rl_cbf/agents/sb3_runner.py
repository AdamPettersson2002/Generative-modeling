"""Stable-Baselines3 experiment orchestration placeholders."""

from dataclasses import dataclass


SUPPORTED_ALGORITHMS = ("dqn", "ppo")


@dataclass(frozen=True)
class AgentRunConfig:
    """Minimal run config before wiring in YAML loading and SB3."""

    algorithm: str
    total_timesteps: int
    policy: str = "MlpPolicy"
    gamma: float = 0.99

    def validate(self) -> None:
        if self.algorithm not in SUPPORTED_ALGORITHMS:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")
        if self.total_timesteps <= 0:
            raise ValueError("total_timesteps must be positive")
