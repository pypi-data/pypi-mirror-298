torch_available = True
import time
from typing import Literal, Callable
try:
    import torch
except ImportError:
    torch_available = False
from contextlib import contextmanager
import logging
from attrs import define

pylogger = logging.getLogger(__name__)

@define
class TimingConfig:
    timing_pre_hook: Callable[[str],None] | None = None
    timing_post_hook: Callable[[str,float],None] | None = None
    executing: bool = True
    cuda_sync: bool = False
    tick_guard: Callable[[], None] | None = None

class Timer:
    def __init__(self, config: TimingConfig):
        self.config = config
        self.records = []
    def pre_timing(self, name):
        if self.config.timing_pre_hook is not None:
            self.config.timing_pre_hook(name)
    def post_timing(self, name, time):
        if self.config.timing_post_hook is not None:
            self.config.timing_post_hook(name, time)
    def tick(self):
        if torch_available and self.config.cuda_sync:
            torch.cuda.synchronize()
        if self.config.tick_guard is not None:
            self.config.tick_guard()
        return time.time()
    def start(self, name):
        if not self.config.executing:
            return
        self.pre_timing(name)
        return self.tick()
    def end(self, name, start_time):
        if not self.config.executing:
            return None
        end = self.tick()
        interval = end - start_time
        self.post_timing(name, interval)
        self.records.append([name, interval])
        return interval
    def reset(self):
        self.records = []

_timer = Timer(TimingConfig())

def set_config(config: TimingConfig):
    """
    Set the global timer config.
    Warning: This will reset the global timer(you will lose all records).
    """
    global _timer
    _timer = Timer(config)

def timethis(name):
    """
    Use as a decorator to record the running time of a function / method.

    example:
    @timethis("my_func")
    def my_func():
        pass
    """
    pylogger.info(f"{name} registered for timing.")

    def dec(func):
        def wrapper(*args, **kwargs):
            start = _timer.start(name)
            result = func(*args, **kwargs)
            _timer.end(name, start)
            return result
        return wrapper
    return dec

def reset():
    _timer.reset()

@contextmanager
def timing(name):
    """
    Use as a context manager to record the running time of a block of code.
    example:
    import witlog.timing as wt

    with wt.timing("my_block"):
        # some code here
        pass
    """
    start = _timer.start(name)
    yield
    _timer.end(name, start)

def get_records(format: Literal["list", "pandas"] = "list", copy = False):
    """
    Get the timing records.

    Records are a list of [name, duration] pairs, sorted by end timing.
    """
    if copy:
        records = _timer.records.copy()
    else:
        records = _timer.records
    if format == "list":
        return records
    elif format == "pandas":
        import pandas as pd

        return pd.DataFrame(records, columns=["name", "duration"])
    else:
        raise ValueError(f"Unsupported format: {format}")
