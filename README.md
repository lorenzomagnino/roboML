After creating a new repository from this template, run `make init` first.

<div align="center">
  <img src="favicon.svg" alt="RoboML Research Template" width="110" height="110">
</div>

<br>
<br>

#  🧩 RoboML Research Template

A lightweight, opinionated template for running machine learning and robotics research projects. It provides a standardized structure for experiments, data handling, logging, and evaluation, with ready-to-use configs and scripts for reproducible workflows.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/badge/uv-package%20manager-purple.svg)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)



## Projects Built with RoboML Research Template

Projects that used RoboML template:

[![proteinRL](https://img.shields.io/badge/lorenzomagnino-proteinRL-4c1d95?style=flat-square&logo=github&logoColor=white)](https://github.com/lorenzomagnino/proteinRL)
[![dedaFP](https://img.shields.io/badge/lorenzomagnino-dedaFP-4c1d95?style=flat-square&logo=github&logoColor=white)](https://github.com/lorenzomagnino/dedaFP)
[![Bench-MFG](https://img.shields.io/badge/lorenzomagnino-Bench--MFG-4c1d95?style=flat-square&logo=github&logoColor=white)](https://github.com/lorenzomagnino/Bench-MFG)

Let me know if you use this template!!


## Features

- **Hydra Configuration Management**: Modular config structure with separate files for model, training, and wandb settings
- **Type-Safe Configs**: Dataclass schemas for configuration validation and IDE support
- **Wandb Integration**: Built-in experiment tracking and logging
- **Fast Package Management**: Uses `uv` for quick dependency installation
- **Development Tools**: Pre-commit hooks with ruff and black for code quality
- **Auto-formatting**: Ruff automatically formats Python files on save (VS Code/Cursor)

## Setup

Use this repository as a GitHub template instead of cloning it directly:

1. Open this repository on GitHub.
2. Click **Use this template** > **Create a new repository**.
3. Choose the owner and repository name for your new research project.
4. Clone your new repository:
```bash
git clone <repository-url>
cd <repository-name>
```
5. Bootstrap the project:
```bash
make init
source .venv/bin/activate
```

Prerequisites: Python 3.8+ and [uv](https://github.com/astral-sh/uv).

### Try it! It's simple
```bash
python main.py
```

### Configuration

Configuration files are located in the `config/` directory:
- `defaults.yaml`: Main defaults file that imports all configs
- `model.yaml`: Model architecture parameters
- `training.yaml`: Training hyperparameters
- `wandb.yaml`: Wandb project settings
- `config.yaml`: General experiment settings

Override config values via command line:
```bash
python main.py training.learning_rate=0.01 training.batch_size=64
```

### Development

- **Lint code**: `make lint`
- **Format code**: `make format`
- **Run tests**: `make test`
- **Clean cache**: `make clean`

### Optional Watson support

[Watson](https://github.com/lorenzomagnino/watson) provides experiment logging
and bag storage. After setup, install it into a Python 3.10+ environment:

```bash
make install-watson
```

This installs a pinned GitHub revision because the current PyPI release lacks
project-config support. Git and access to the private Watson repository are required.

Edit [`watson.yaml`](watson.yaml) to set the bag destination (`bags_dir`) and
optional W&B project, entity, run name, group, and tags. Relative destinations
resolve from that file's directory; the default `bags/` is ignored by Git.
Run commands from this repo or a subdirectory so Watson discovers the file:

```bash
.venv/bin/watson save /path/to/completed/recording --name experiment
.venv/bin/watson list
```

`WATSON_BAGS` or `watson --root /another/destination ...` overrides `bags_dir`.
For W&B logging, authenticate with `wandb login` or `WANDB_API_KEY`, then attach
the configured handler in your experiment code:

```python
import watson as wt

settings = wt.load_project_config()
wt.attach(wt.WandBHandler(**settings.wandb))
try:
    logger = wt.get_logger("experiment", with_metrics=True)
    logger.scalar("loss", 0.12, step=1)
finally:
    wt.finish()
```

Use this handler instead of also calling `init_wandb` for the same run.
Watson's W&B settings are separate from Hydra's `logging.wandb` config and
are only activated when you attach the handler.

## Project Structure

```
roboml-research-template/
├── config/              # Hydra configuration files
│   ├── config_schema.py # Dataclass schemas
│   ├── defaults.yaml    # Main defaults
│   ├── model.yaml       # Model config
│   ├── training.yaml    # Training config
│   ├── wandb.yaml       # Wandb config
│   └── config.yaml      # General config
├── networks/            # Network architectures
├── learner/             # Learning algorithms
├── tests/               # Test files
└── main.py              # Entry point
```



## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

See LICENSE file for details.
