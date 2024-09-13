from typing import List, Type
from src.game_objects.game_object import GameObject
from src.game_objects.power_game_object import PowerGameObject
from src.game_objects.life_power_game_object import LifePowerGameObject
from src.game_objects.skull_power_game_object import SkullPowerGameObject
from src.game_objects.block_game_object import BlockGameObject
from src.sprites.block_sprites import SimpleSprite
from src.scenes.scene import Scene
from typing import Dict, Callable
import random
from config import PROBABILITY_SPAWN_POWER

class BrokenBlockGameObject(BlockGameObject):
  POWERS: List[Type[PowerGameObject]] = [
    LifePowerGameObject,
    SkullPowerGameObject,
  ]

  def __init__(
      self,
      sprites: SimpleSprite,
      scene: Scene,
      x: float,
      y: float,
      order_in_layer: int,
      layers: List[str] = [],
    ) -> None:
    super().__init__(sprites, scene, x, y, order_in_layer, layers)
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
        scene = self._scene,
        x = self._x + self._sprites.width() / 4,
        y = self._y + self._sprites.height() / 4,
        size = (self._sprites.width() / 2, self._sprites.height() / 2),
      )

    self.destroy()

