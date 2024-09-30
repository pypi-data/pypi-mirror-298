#!/usr/bin/env python3

from queue import SimpleQueue
from enum import IntEnum
from threading import Thread, Semaphore
from garagedoor_service.gpio.GPIOAdapter import GPIOAdapter
import time


# Maximum Queue Sizea
QUEUESIZE: int = 3
TOGGLEDELAY: float = .25


# Module scoped queue used to send commands to the door controller.
__queue: SimpleQueue = SimpleQueue()
__queueSem: Semaphore = Semaphore(QUEUESIZE)
__gpioAdapter: GPIOAdapter = None
__thread: Thread = None
__running: bool = False


class QueueElement(IntEnum):
    """Queue elements used to communicate with the door controller."""
    TOGGLE = 1


def door_controller() -> None:
    """Door controller coroutine that processes commands from the queue."""
    global __running
    global __gpioAdapter
    global __queue
    global __queueSem
    
    while __running:
        # Wait for a command to be placed in the queue.
        command = __queue.get()
        __queueSem.release()

        # Toggle the door motor.
        if command == QueueElement.TOGGLE:
            __gpioAdapter.writeTogglePin(True)
            time.sleep(TOGGLEDELAY)
            __gpioAdapter.writeTogglePin(False)
            time.sleep(TOGGLEDELAY) # Backoff from processing more commands.
            
            
def start_door_controller(gpioAdapter: GPIOAdapter) -> None:
    """Start the door controller coroutine.
    Args:
        gpioAdapter (GPIOAdapter): The GPIO adapter to use to control the door.
    """
    global __thread
    global __gpioAdapter
    global __running
    
    __gpioAdapter = gpioAdapter
    __running = True
    __thread = Thread(target=door_controller, daemon=True).start()


def stop_door_controller() -> None:
    """Stop the door controller coroutine."""
    global __running
    global __thread
    
    __running = False
    __thread.join()


def request_door_toggle() -> None:
    """Request the door controller to toggle the door's motor."""
    if __queueSem.acquire(blocking=False):
        __queue.put_nowait(QueueElement.TOGGLE)
    
    
def get_door_state() -> str:
    """Get the current state of the door.
    Returns:
        str: The state of the door (open, closed or unknown).
    """
    openState: bool = __gpioAdapter.readOpenPin()
    closedState: bool = __gpioAdapter.readClosePin()
    if openState and not closedState:
        return "open"
    if closedState and not openState:
        return "closed"
    return "unknown"
