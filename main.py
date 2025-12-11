import argparse

from src.orchestrator import core

def _parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config", type=str, help="Yaml configuration file path")
    args = parser.parse_args()

    if not args.config:
        parser.print_help()
        raise RuntimeError("Configuration file not specified")

    return args


if __name__ == "__main__":
    args = _parse_arguments()

    core(args.config)