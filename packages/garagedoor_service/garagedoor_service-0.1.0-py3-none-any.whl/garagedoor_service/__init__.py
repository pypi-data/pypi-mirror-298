#!/usr/bin/env python3

from garagedoor_service.gpio import GPIOAdapter, GPIOMockAdapter, GPIOPiAdapter
import garagedoor_service.door_controller as door_controller
import garagedoor_service.tools.config as config

config.load_config()

__mode = config.get_mode()
if __mode == "development":
    __gpioAdapter: GPIOAdapter = GPIOMockAdapter(
        config.get_toggle_pin(),
        config.get_open_pin(),
        config.get_closed_pin())
elif __mode == "production":
    __gpioAdapter: GPIOAdapter = GPIOPiAdapter(
        config.get_toggle_pin(),
        config.get_open_pin(),
        config.get_closed_pin())
else:
    raise ValueError(f"Invalid mode in configuration: {__mode}")

door_controller.start_door_controller(__gpioAdapter)