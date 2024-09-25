from zest.releaser import pypi
from zestreleaser.towncrier import _load_config

import os


class Style:
    RED = "\033[31m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    RESET = "\033[0m"


def get_default_location():
    """Get the default configuration."""
    default_location = None
    setup_cfg = pypi.SetupConfig()
    config = setup_cfg.config
    if config and config.has_option("zest.releaser", "history_file"):
        default_location = config.get("zest.releaser", "history_file")
    return default_location


def get_towncrier_config():
    """Get the towncrier configuration."""
    full_config = _load_config()
    config = full_config["tool"]["towncrier"]
    return config


def get_towncrier_directory():
    config = get_towncrier_config()
    # Where are the snippets stored?
    directory = config.get("directory")
    if not directory:
        # Look for "newsfragments" directory.
        # We could look in the config file, but I wonder if that may change,
        # so simply look for a certain directory name.
        fragment_directory = "news"
        for dirpath, dirnames, filenames in os.walk("."):
            if dirpath.startswith(os.path.join(".", ".")):
                # for example ./.git
                continue
            if fragment_directory in dirnames:
                directory = os.path.join(dirpath, fragment_directory)
                break
        if not directory:
            # Either towncrier won't work, or our logic is off.
            print("WARNING: could not find news directory for towncrier.")
            return
    return directory


def get_towncrier_types() -> list:
    """Get the towncrier issue types."""
    config = get_towncrier_config()
    if "type" in config:
        types = [entry.get("directory") for entry in config["type"]]
    else:
        # towncrier._settings._default_types seems too private to depend on,
        # so hardcopy it.
        types = ["feature", "bugfix", "breaking", "internal", "documentation", "tests"]

    return types
