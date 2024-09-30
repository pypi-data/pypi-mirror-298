#!/usr/bin/env python3

from abc import ABC, abstractmethod

class GPIOAdapter(ABC):
    """Interface for GPIO operations."""
    
    def __init__(self, doorPin: int, doorOpenPin: int, doorClosePin: int) -> None:
        """Initialize the GPIO interface.
        Parameters:
            doorPin (int): The pin to control the door motor.
            doorOpenPin (int): The pin to read the door open state.
            doorClosePin (int): The pin to read the door close state.
        """
        self._doorPin = doorPin
        self._doorOpenPin = doorOpenPin
        self._doorClosePin = doorClosePin


    @abstractmethod
    def writeTogglePin(self, state: bool) -> None:
        """Set the pin state for the DoorTogglePin.
        Parameters:
            state (bool): The state to set the pin to.
        """
        pass


    @abstractmethod
    def readOpenPin(self) -> bool:
        """Read the pin state of the doorOpenPin.
        Returns:
            bool: The state of the pin.
        """
        pass
    
    
    @abstractmethod
    def readClosePin(self) -> bool:
        """Read the pin state of the doorClosePin.
        Returns:
            bool: The state of the pin.
        """
        pass
