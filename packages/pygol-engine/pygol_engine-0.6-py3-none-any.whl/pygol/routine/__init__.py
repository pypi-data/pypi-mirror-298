import threading
import time, multiprocessing
from pygol.drawable import Drawable

def _run_async_void(millis, void, repeats):
    if repeats > 0:
        for _ in range(repeats):
            time.sleep(millis/1000)
            void()
    elif repeats <= 0:
        while True:
            time.sleep(millis/1000)
            void()

def perform_with_delay(millis, target, times=1):
    threading.Thread(target=_run_async_void, args=(millis, target, times), daemon=True).start()

import time

def buffered_transite(obj: Drawable, x: int, y: int, seconds: int):
    dx = x - obj.x
    dy = y - obj.y
    
    steps = int(seconds * 100)
    x_step = dx / steps
    y_step = dy / steps
    
    for _ in range(steps):
        obj.x += x_step
        obj.y += y_step
        time.sleep(seconds / steps)

def transite_to(obj: Drawable, x: int, y: int, seconds: int):
    threading.Thread(target=buffered_transite, args=(obj, x, y, seconds), daemon=True).start()
    