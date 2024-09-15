from typing import Tuple, Callable, Dict
from src.core.game_object import GameObject
from src.game_objects.player_game_object import PlayerGameObject
from src.game_objects.power_game_object import PowerGameObject
from src.sprites.block_sprites import SimpleSprite
from os.path import join
from src.enums.power_enum import PowerEnum

class LifePowerGameObject(PowerGameObject):
  def __init__(
      self,
      x: float,
      y: float,
      size: Tuple[int, int],
      min_x: float = -float('inf'),
      max_x: float = float('inf'),
      min_y: float = -float('inf'),
      max_y: float = float('inf'),
    ) -> None:
    super().__init__(x, y, size, PowerEnum.LIFE, min_x, max_x, min_y, max_y)

  def on_collide(self, other: GameObject, layer: str) -> None:
    handlers: Dict[str, Callable] = {
      'player1_power': lambda: self.__handle_life_power_layer(other),
      'player2_power': lambda: self.__handle_life_power_layer(other),
    }
    if layer in handlers:
      handlers[layer]()

  def _define_sprites(self) -> SimpleSprite:
    return SimpleSprite(join(self._type.base_dir(), 'life_power.png'), self._size)

  def __handle_life_power_layer(self, other: PlayerGameObject) -> None:
    other.set_lives(other.get_lives() + 1)
    self.destroy()
