#!/usr/bin/env python3

from garagedoor_service.gpio.GPIOAdapter import GPIOAdapter

class GPIOPiAdapter(GPIOAdapter):
    def __init__(self, doorPin: int, doorOpenPin: int, doorClosePin: int) -> None:
        super().__init__(doorPin, doorOpenPin, doorClosePin)
        
        from RPi import GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._doorPin, GPIO.OUT)
        GPIO.setup(self._doorOpenPin, GPIO.IN)
        GPIO.setup(self._doorClosePin, GPIO.IN)
        
        
    def __del__(self):
        from RPi import GPIO
        GPIO.cleanup()
    
    
    def writeTogglePin(self, state: bool) -> None:
        from RPi import GPIO
        GPIO.output(self._doorPin, state)


    def readOpenPin(self) -> bool:
        from RPi import GPIO
        return GPIO.input(self._doorOpenPin)
    
    
    def readClosePin(self) -> bool:
        from RPi import GPIO
        return GPIO.input(self._doorClosePin)