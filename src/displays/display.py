from abc import ABC, abstractmethod
import pygame

class Display(ABC):
  def __init__(self, screen: pygame.Surface) -> None:
    self._screen = screen

  @abstractmethod
  def start(self) -> None:
    pass

  @abstractmethod
  def update(self) -> None:
    pass

  @abstractmethod
  def height(self) -> float:
    pass
