#!/usr/bin/env python3

from yaml import safe_load
import os

__config: dict = None

def load_config() -> None:
    """Load the configuration from the config.yaml or file defined by $GARAGEDOOR_SERVICE_CONFIG file."""
    global __config
    path = os.getenv("GARAGEDOOR_SERVICE_CONFIG")
    if path is None:
        path = "config.yaml"
    with open(path, "r") as file:
        __config = safe_load(file)
        
        
def get_api_keys() -> list[str]:
    """Get the list of API keys from the configuration.
    Returns:
        list[str]: The list of API keys. API keys will be bcrypt hashed.
    """
    return __config["api_keys"]


def get_mode() -> str:
    """Get the mode from the configuration.
    Returns:
        str: The mode.
    """
    return __config["mode"]


def get_toggle_pin() -> int:
    """Get the pin to control the door motor from the configuration.
    Returns:
        int: The pin to control the door motor.
    """
    return __config["gpio"]["toggle_pin"]


def get_open_pin() -> int:
    """Get the pin to read the door open state from the configuration.
    Returns:
        int: The pin to read the door open state.
    """
    return __config["gpio"]["open_pin"]


def get_closed_pin() -> int:
    """Get the pin to read the door close state from the configuration.
    Returns:
        int: The pin to read the door close state.
    """
    return __config["gpio"]["closed_pin"]


def get_bind_host() -> str:
    """Get the bind address from the configuration.
    Returns:
        str: The bind address.
    """
    return __config["bind"]["host"]


def get_bind_port() -> int:
    """Get the bind port from the configuration.
    Returns:
        int: The bind port.
    """
    return __config["bind"]["port"]