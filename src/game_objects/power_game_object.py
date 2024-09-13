from abc import abstractmethod
from typing import List, Tuple
from src.game_objects.game_object import GameObject
from src.sprites.block_sprites import SimpleSprite
from src.scenes.scene import Scene
import pygame
from config import POWER_GAME_OBJECT_ORDER_IN_LAYER

class PowerGameObject(GameObject):
  def __init__(
      self,
      scene: Scene,
      x: float,
      y: float,
      size: Tuple[int, int],
    ) -> None:
    self._size = size
    order_in_layer = POWER_GAME_OBJECT_ORDER_IN_LAYER
    sprites = self._define_sprites()
    layers = self._define_layers()

    super().__init__(sprites, scene, x, y, order_in_layer, layers)
    self._sprites = sprites

  @GameObject._start_decorator
  def start(self) -> None:
    self._current_sprite: pygame.Surface = self._sprites.idle()

  def update(self) -> None:
    return

  def on_collide(self, other: GameObject, layer: str) -> None:
    return

  @abstractmethod
  def _define_sprites(self) -> SimpleSprite:
    pass
  
  def _define_layers(self) -> List[str]:
    return ['player1_power', 'player2_power']