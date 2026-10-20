import subprocess
import sys
from pathlib import Path

from hydra import compose, initialize_config_dir
from omegaconf import OmegaConf

import init_project
from config import Config

ROOT = Path(__file__).resolve().parents[1]


def test_initializer():
    init_project.self_test()


def test_config_contains_only_environment_and_training_groups():
    with initialize_config_dir(version_base=None, config_dir=str(ROOT / "config")):
        cfg = compose(config_name="defaults", overrides=["training.batch_size=8"])
    cfg = OmegaConf.merge(OmegaConf.structured(Config), cfg)
    assert set(cfg) == {"environment", "training", "experiment_name", "seed", "device"}
    assert cfg.training.batch_size == 8


def test_main_runs_without_writing_logs_or_outputs(tmp_path):
    result = subprocess.run(
        [sys.executable, str(ROOT / "main.py"), "training.batch_size=8"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    )
    assert "batch_size: 8" in result.stdout
    assert list(tmp_path.iterdir()) == []
