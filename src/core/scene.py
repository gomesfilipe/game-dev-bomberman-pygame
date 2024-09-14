import pygame
from abc import ABC, abstractmethod
from typing import Tuple, Optional
from src.core.display import Display
from src.core.game_object_manager import GameObjectManager
from src.core.game_object import GameObject

class Scene(ABC):
  def __init__(self, screen: Tuple[int, int], display: Optional[Display] = None) -> None:
    self._screen: pygame.Surface = screen
    self._display = display
    self._game_object_manager = GameObjectManager()

  @abstractmethod
  def start_scene(self) -> None:
    pass

  def update_scene(self) -> None:
    if self._display is not None:
      self._display.update()

    self._game_object_manager.update()
    self._game_object_manager.draw()

  def get_screen(self) -> pygame.Surface:
    return self._screen

  def get_display(self) -> Optional[Display]:
    return self._display

  def switch_debug_mode(self) -> None:
    self._game_object_manager.switch_debug_mode()

  def add_game_object(self, game_object: GameObject) -> None:
    self._game_object_manager.add(game_object)

  def remove_game_object(self, game_object: GameObject) -> None:
    self._game_object_manager.remove(game_object)
