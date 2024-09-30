#!/usr/bin/env python3

from garagedoor_service.gpio.GPIOAdapter import GPIOAdapter

class GPIOMockAdapter(GPIOAdapter):
    """Mock GPIO adapter for testing."""
    
    def __init__(self, doorPin: int, doorOpenPin: int, doorClosePin: int) -> None:
        super().__init__(doorPin, doorOpenPin, doorClosePin)
        print("Mock: Initialized")
        self.__doorOpenPinState = False
        self.__doorClosePinState = True
    
    
    def writeTogglePin(self, state: bool) -> None:
        print(f"Mock: Set pin {self._doorPin} to {state}")
        if state:
            self.__doorOpenPinState = not self.__doorOpenPinState
            self.__doorClosePinState = not self.__doorClosePinState


    def readOpenPin(self) -> bool:
        print (f"Mock: Read pin {self._doorOpenPin}, state is {self.__doorOpenPinState}")
        return self.__doorOpenPinState
    
    
    def readClosePin(self) -> bool:
        print (f"Mock: Read pin {self._doorClosePin}, state is {self.__doorClosePinState}")
        return self.__doorClosePinState
