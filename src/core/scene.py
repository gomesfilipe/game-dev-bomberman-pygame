from src.core.base_object import BaseObject
import pygame
from typing import Tuple, Optional
from src.core.display import Display
from src.core.game_object_manager import GameObjectManager
from src.core.game_object import GameObject

class Scene(BaseObject):
  def __init__(
    self,
    width: float,
    height: float,
    tiles_width: int,
    tiles_height: int,
    display: Optional[Display] = None,
    background_color: str = 'white',
  ) -> None:
    self._width = width
    self._height = height
    self._tiles_width = tiles_width
    self._tiles_height = tiles_height
    self._display = display
    self._background_color = background_color
    self._game_object_manager = GameObjectManager(self._tiles_width, self._tiles_height)

  def on_end_scene(self) -> None:
    return

  def width(self) -> float:
    return self._width

  def height(self) -> float:
    return self._height

  def update(self) -> None:
    if self._display is not None:
      self._display.update()

    self._game_object_manager.update()

  def fixed_update(self) -> None:
    return

  def draw(self, screen: pygame.Surface) -> None:
    screen.fill(self._background_color)

    if self._display is not None:
      self._display.draw(screen)

    self._game_object_manager.draw(screen)
    pygame.display.flip()

  def get_display(self) -> Optional[Display]:
    return self._display

  def switch_debug_mode(self) -> None:
    self._game_object_manager.switch_debug_mode()

  def add_game_object(self, game_object: GameObject) -> None:
    self._game_object_manager.add_game_object(game_object)

  def remove_game_object(self, game_object: GameObject) -> None:
    self._game_object_manager.remove_game_object(game_object)
