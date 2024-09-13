from typing import List, Tuple, Callable, Dict
from src.game_objects.game_object import GameObject
from src.game_objects.player_game_object import PlayerGameObject
from src.game_objects.power_game_object import PowerGameObject
from src.sprites.block_sprites import SimpleSprite
from src.scenes.scene import Scene
from os.path import join
from src.enums.event_enum import EventEnum

class SkullPowerGameObject(PowerGameObject):
  def __init__(
      self,
      scene: Scene,
      x: float,
      y: float,
      size: Tuple[int, int],
    ) -> None:
    super().__init__(scene, x, y, size)

  def on_collide(self, other: GameObject, layer: str) -> None:
    handlers: Dict[str, Callable] = {
      'player1_power': lambda: self.__handle_power_layer(other),
      'player2_power': lambda: self.__handle_power_layer(other),
    }
    if layer in handlers:
      handlers[layer]()

  def _define_sprites(self) -> SimpleSprite:
    return SimpleSprite(join('assets', 'powers', 'skull_power.png'), self._size)

  def __handle_power_layer(self, other: PlayerGameObject) -> None:
    other.set_lives(other.get_lives() - 1)
    player_name = other.get_name()
    self.destroy()
    EventEnum.SKULL_POWER_COLLECTED.post_event(player_name = player_name)
