from abc import ABC, abstractmethod
from src.core.game_object import GameObject
from typing import Callable
import time

class Skill(ABC):
  def __init__(self, cdr: float) -> None:
    self._cdr = cdr
    self._last_use: float = time.time() - self._cdr

  def _can_execute(self) -> bool:
    return time.time() - self._last_use >= self._cdr

  def set_cdr(self, cdr: float) -> None:
    self._cdr = cdr

  def _execute_decorator(func: Callable) -> Callable:
    def manage_cdr(self: 'Skill', game_object: GameObject) -> None:
      if self._can_execute():
        func(self, game_object)
        self._last_use = time.time()

    return manage_cdr

  @abstractmethod
  def execute(self, game_object: GameObject) -> None:
    pass
