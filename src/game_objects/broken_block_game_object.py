from typing import List
from src.core.game_object import GameObject
from src.game_objects.block_game_object import BlockGameObject
from src.sprites.simple_sprite import SimpleSprite
from typing import Dict, Callable
import random
from config import PROBABILITY_SPAWN_POWER
from src.game_objects.power_game_object import PowerGameObject
from src.game_objects.life_power_game_object import LifePowerGameObject
from src.game_objects.skull_power_game_object import SkullPowerGameObject
from src.game_objects.drop_bomb_cdr_power_game_object import DropBombCdrPowerGameObject
from src.game_objects.increase_explosion_range_power_game_object import IncreaseExplosionRangePowerGameObject
from src.game_objects.super_bomb_power_game_object import SuperBombPowerGameObject
from src.enums.game_object_type_enum import GameObjectTypeEnum

class BrokenBlockGameObject(BlockGameObject):
  __POWERS: List[PowerGameObject] = [
    LifePowerGameObject,
    SkullPowerGameObject,
    DropBombCdrPowerGameObject,
    IncreaseExplosionRangePowerGameObject,
    SuperBombPowerGameObject,
  ]

  def __init__(
      self,
      sprites: SimpleSprite,
      x: float,
      y: float,
      order_in_layer: int,
      game_object_type: GameObjectTypeEnum,
      layers: List[str] = [],
      min_x: float = -float('inf'),
      max_x: float = float('inf'),
      min_y: float = -float('inf'),
      max_y: float = float('inf'),
    ) -> None:
    super().__init__(sprites, x, y, order_in_layer, game_object_type, layers, min_x, max_x, min_y, max_y)
    self._spawn_probability = PROBABILITY_SPAWN_POWER

  def on_collide(self, other: GameObject, layer: str) -> None:
    handlers: Dict[str, Callable] = {
      'explosion': lambda: self.__handle_player_explosion_layer(other),
    }

    if layer in handlers:
      handlers[layer]()

  def __handle_player_explosion_layer(self, other: GameObject) -> None:
    if self.__should_spawn_power():
      power_class = random.choice(BrokenBlockGameObject.__POWERS)

      self.instantiate(
        power_class,
        x = self._x + self._sprites._hitbox.get_width() / 4,
        y = self._y + self._sprites._hitbox.get_height() / 4,
        size = (self._sprites._hitbox.get_width() / 2, self._sprites._hitbox.get_height() / 2),
        game_object_type = GameObjectTypeEnum.TILE,
        min_x = self._min_x,
        max_x = self._max_x,
        min_y = self._min_y,
        max_y = self._max_y,
      )

    self.destroy()

  def __should_spawn_power(self) -> bool:
    return random.uniform(0, 1) <= self._spawn_probability
