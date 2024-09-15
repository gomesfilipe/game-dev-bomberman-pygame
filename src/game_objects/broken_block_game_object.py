from typing import List, Type
from src.core.game_object import GameObject
from src.game_objects.power_game_object import PowerGameObject
from src.game_objects.life_power_game_object import LifePowerGameObject
from src.game_objects.skull_power_game_object import SkullPowerGameObject
from src.game_objects.block_game_object import BlockGameObject
from src.sprites.block_sprites import SimpleSprite
from src.core.display import Display
from typing import Dict, Callable
import random
from config import PROBABILITY_SPAWN_POWER
import pygame

class BrokenBlockGameObject(BlockGameObject):
  POWERS: List[Type[PowerGameObject]] = [
    LifePowerGameObject,
    SkullPowerGameObject,
  ]

  def __init__(
      self,
      sprites: SimpleSprite,
      x: float,
      y: float,
      order_in_layer: int,
      layers: List[str] = [],
      min_x: float = -float('inf'),
      max_x: float = float('inf'),
      min_y: float = -float('inf'),
      max_y: float = float('inf'),
    ) -> None:
    super().__init__(sprites, x, y, order_in_layer, layers, min_x, max_x, min_y, max_y)
    self._spawn_probability = PROBABILITY_SPAWN_POWER

  def on_collide(self, other: GameObject, layer: str) -> None:
    handlers: Dict[str, Callable] = {
      'player1_broken_block': lambda: self.__handle_player_broken_block_layer(other),
      'player2_broken_block': lambda: self.__handle_player_broken_block_layer(other),
    }

    if layer in handlers:
      handlers[layer]()

  def __handle_player_broken_block_layer(self, other: GameObject) -> None:
    if random.uniform(0, 1) <= self._spawn_probability:
      power_class: Type[PowerGameObject] = random.choice(BrokenBlockGameObject.POWERS)

      self.instantiate(
        power_class,
        x = self._x + self._sprites.width() / 4,
        y = self._y + self._sprites.height() / 4,
        size = (self._sprites.width() / 2, self._sprites.height() / 2),
        min_x = self._min_x,
        max_x = self._max_x,
        min_y = self._min_y,
        max_y = self._max_y,
      )

    self.destroy()
