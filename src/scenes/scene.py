import pygame
from abc import ABC, abstractmethod
from typing import Tuple, Optional
from src.displays.display import Display

class Scene(ABC):
  def __init__(self, screen: Tuple[int, int], display: Optional[Display] = None) -> None:
    self._screen: pygame.Surface = screen
    self._display = display


  @abstractmethod
  def start_scene(self) -> None:
    pass

  @abstractmethod
  def update_scene(self) -> None:
    pass

  def get_screen(self) -> pygame.Surface:
    return self._screen

  def get_display(self) -> Optional[Display]:
    return self._display
