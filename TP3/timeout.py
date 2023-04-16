import time
import signal

from typing import NamedTuple, ContextManager, List
from contextlib import contextmanager

class _Timer(NamedTuple):
    expiration: float
    exception: Exception

__timers: List[_Timer] = []

class Quota(object):
    def __init__(self, seconds: float) -> None:
        if seconds <= 0:
            raise ValueError(f"Invalid timeout: {seconds}")
        else:
            self._timeleft = seconds
        self._depth = 0
        self._starttime = None

    def __str__(self) -> str:
        return f"<Quota remaining={self.remaining()}>"
    
    def _start(self) -> None:
        if self._depth == 0:
            self._starttime = time.perf_counter_ns()
        self._depth += 1

    def _stop(self) -> None:
        if self._depth == 1:
            self._timeleft = self.remaining()
            self._starttime = None
        self._depth -= 1

    def running(self) -> bool:
        return self._depth > 0
    
    def remaining(self):
        if self.running():
            return max(self._timeleft - (time.time() - self._starttime), 0)
        else:
            return max(self._timeleft, 0)


def _handler(*args):
    exception = __timers.pop().exception
    if __timers:
        timeleft = __timers[-1].expiration - time.time()
        if timeleft > 0:
            signal.setitimer(signal.ITIMER_REAL, timeleft)
        else:
            _handler(*args)
    raise exception


def _set_sighandler():
    current = signal.getsignal(signal.SIGALRM)
    if current == signal.SIG_DFL:
        signal.signal(signal.SIGALRM, _handler)

@contextmanager
def timeout(seconds: float, exception: Exception = RuntimeError) -> ContextManager[None]:
    if isinstance(seconds, Quota):
        quota = seconds
    else:
        quota = Quota(float(seconds))
    _set_sighandler()
    seconds = quota.remaining()

    depth = len(__timers)
    parent_time_left = signal.getitimer(signal.ITIMER_REAL)[0]
    if not __timers or parent_time_left > seconds:
        try:
            quota._start()
            __timers.append(_Timer(time.time() + seconds, exception))
            if seconds > 0:
                signal.setitimer(signal.ITIMER_REAL, seconds)
                yield
            else:
                _handler()
        finally:
            quota._stop()
            if len(__timers) > depth:
                # Cancel the timer
                signal.setitimer(signal.ITIMER_REAL, 0)
                __timers.pop()
                if __timers:
                    parent_time_left = __timers[-1].expiration - time.time()
                    if parent_time_left > 0:
                        signal.setitimer(signal.ITIMER_REAL, parent_time_left)
                    else:
                        _handler()
    else:
        # Not enough time left on the parent timer
        try:
            quota._start()
            yield
        finally:
            quota._stop()
