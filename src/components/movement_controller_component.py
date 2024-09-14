from src.core.component import Component
import math
from src.utils.utils import lerp
from typing import Dict, Callable
from src.utils.movement_commands import MovementCommands
from src.enums.direction_enum import DirectionEnum

class MovementControllerComponent(Component):
  pass

from src.core.game_object import GameObject
import pygame

class MovementControllerComponent(Component):
  def __init__(self, game_object: GameObject, name: str = ''):
    super().__init__(game_object, name)

    if self._game_object._commands is None:
      self._commands = MovementCommands(pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT)
    else:
      self._commands = self._game_object._commands

    self._key_handlers = self.__key_handlers()

  def draw(self, screen: pygame.Surface):
    return

  def start(self) -> None:
    return

  def update(self) -> None:
    self.__handle_pressed_keys()

  def fixed_update(self) -> None:
    return

  def __vertical_move(self, angle: int) -> None:
    self._game_object._theta = math.radians(angle)
    self._game_object._vy = self._game_object._velocity * math.sin(self._game_object._theta)
    self._game_object._previous_y = self._game_object._y
    self._game_object._y = lerp(
      self._game_object._y + self._game_object._vy * self._game_object._delta_time,
      self._game_object._display.height(),
      self._game_object._screen.get_height() - self._game_object._sprites._hitbox.get_height()
    )

  def __horizontal_move(self, angle: int) -> None:
    self._game_object._theta = math.radians(angle)
    self._game_object._vx = self._game_object._velocity * math.cos(self._game_object._theta)
    self._game_object._previous_x = self._game_object._x
    self._game_object._x = lerp(self._game_object._x + self._game_object._vx * self._game_object._delta_time, 0, self._game_object._screen.get_width() - self._game_object._sprites._hitbox.get_width())

  def __move_up(self) -> None:
    self.__vertical_move(-90)
    self._game_object._direction = DirectionEnum.UP

  def __move_down(self) -> None:
    self.__vertical_move(90)
    self._game_object._direction = DirectionEnum.DOWN

  def __move_left(self) -> None:
    self.__horizontal_move(-180)
    self._game_object._direction = DirectionEnum.LEFT

  def __move_right(self) -> None:
    self.__horizontal_move(0)
    self._game_object._direction = DirectionEnum.RIGHT

  def __key_handlers(self) -> Dict[str, Callable]:
    return {
      self._commands.up(): self.__move_up,
      self._commands.down(): self.__move_down,
      self._commands.left(): self.__move_left,
      self._commands.right(): self.__move_right,
    }

  def __handle_pressed_keys(self) -> None:
    pressed_keys = pygame.key.get_pressed()

    for key, handler in self._key_handlers.items():
      if pressed_keys[key]:
        handler()
