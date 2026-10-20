"""Main entry point for the research template."""

import hydra
from omegaconf import DictConfig, OmegaConf


@hydra.main(version_base=None, config_path="config", config_name="defaults")
def main(cfg: DictConfig) -> None:
    """Main function with Hydra configuration."""

    print(OmegaConf.to_yaml(cfg))

    # TODO: Add your training/inference logic here


if __name__ == "__main__":
    main()
