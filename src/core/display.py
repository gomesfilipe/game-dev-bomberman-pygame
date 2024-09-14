from src.core.base_object import BaseObject
from abc import abstractmethod
import pygame

class Display(BaseObject):
  def __init__(self, screen: pygame.Surface) -> None:
    self._screen = screen

  @abstractmethod
  def height(self) -> float:
    pass

  def width(self) -> float:
    return self._screen.get_width()

  def update(self) -> None:
    return

  def fixed_update(self) -> None:
    return