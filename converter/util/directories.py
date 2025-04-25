from pathlib import Path

from loguru import logger


def get_project_root() -> Path:
    """
    Helper function to get the root directory of the project.

    :return: project root as ``Path``
    """
    return Path(__file__).parent.parent.parent


if __name__ == "__main__":
    logger.debug(f"Root directory: {get_project_root()}")
