from src.core.component import Component
import math
from src.utils.utils import lerp
from typing import Dict, Callable
from src.commands.skill_commands import SkillCommands
from src.game_objects.bomb_game_object import BombGameObject
from config import BOMB_ORDER_IN_LAYER, EXPLOSION_TIME, EXPLOSION_RANGE, KICK_RANGE
from src.core.game_events import GameEvents

class SkillControllerComponent(Component):
  pass

from src.core.game_object import GameObject
import pygame

class SkillControllerComponent(Component):
  def __init__(self, game_object: GameObject, name: str = ''):
    super().__init__(game_object, name)

    if self._game_object._movement_commands is None:
      self._commands = SkillCommands(pygame.K_p)
    else:
      self._commands = self._game_object._skill_commands

    self._key_handlers = self.__key_handlers()

  def draw(self, screen: pygame.Surface):
    return

  def start(self) -> None:
    return

  def update(self) -> None:
    self.__handle_down_key()

  def fixed_update(self) -> None:
    return

  def __drop_bomb(self) -> None:
    self._game_object.instantiate(
      BombGameObject,
      x = self._game_object._x,
      y = self._game_object._y,
      size = (self._game_object._sprites._hitbox.get_width(), self._game_object._sprites._hitbox.get_height()),
      order_in_layer = BOMB_ORDER_IN_LAYER,
      explosion_time = EXPLOSION_TIME,
      explosion_range = EXPLOSION_RANGE,
      kick_range = KICK_RANGE,
      layers = [],
      min_x = self._game_object._min_x,
      max_x = self._game_object._max_x,
      min_y = self._game_object._min_y,
      max_y = self._game_object._max_y,
    )

  def __key_handlers(self) -> Dict[str, Callable]:
    return {
      self._commands.drop_bomb(): self.__drop_bomb,
    }

  def __handle_down_key(self) -> None:
    event = GameEvents.find(lambda event: event.type == pygame.KEYDOWN)

    if event is None:
      return

    if event.key in self._key_handlers:
      self._key_handlers[event.key]()
