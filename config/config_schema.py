"""Configuration schemas using dataclasses for type safety."""

from dataclasses import dataclass, field

from config.environment.environment_schema import EnvironmentConfig
from config.training.training_schema import TrainingConfig


@dataclass
class Config:
    """Root configuration combining all sub-configs."""

    environment: EnvironmentConfig = field(default_factory=EnvironmentConfig)
    training: TrainingConfig = field(default_factory=TrainingConfig)
    experiment_name: str = "default_experiment"
    seed: int = 42
    device: str = "cpu"  # cpu, cuda
