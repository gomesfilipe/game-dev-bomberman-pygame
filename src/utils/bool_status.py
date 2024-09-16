import time

class BoolStatus:
  def __init__(self, active: bool, duration: float) -> None:
    self._active = active
    self._last_active: float = time.time() if self._active else 0.0
    self._duration = duration

  def is_active(self) -> bool:
    return self._active

  def last_active(self) -> float:
    return self._last_active

  def set_active(self, active: bool) -> None:
    self._active = active

    if self._active:
      self._last_active = time.time()

  def update(self) -> None:
    if self._active and time.time() - self._last_active >= self._duration:
      self._active = False

