from typing import Tuple, Optional
from src.scenes.scene import Scene
from src.displays.display import Display
import pygame

class MainScene(Scene):
  def __init__(self, screen: pygame.Surface, display: Optional[Display] = None) -> None:
    super().__init__(screen, display)

  def start_scene(self) -> None:
    if self._display is not None:
      self._display.start()

  def update_scene(self) -> None:
    if self._display is not None:
      self._display.update()

