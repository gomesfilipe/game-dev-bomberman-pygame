from src.core.game_object import GameObject
from abc import abstractmethod
from typing import List, Tuple
from src.sprites.simple_sprite import SimpleSprite
import pygame
from config import POWER_GAME_OBJECT_ORDER_IN_LAYER
from src.components.sprite_renderer_component import SpriteRendererComponent
from src.enums.power_enum import PowerEnum

class PowerGameObject(GameObject):
  def __init__(
      self,
      x: float,
      y: float,
      size: Tuple[int, int],
      type: PowerEnum,
      min_x: float = -float('inf'),
      max_x: float = float('inf'),
      min_y: float = -float('inf'),
      max_y: float = float('inf'),
    ) -> None:
    self._size = size
    order_in_layer = POWER_GAME_OBJECT_ORDER_IN_LAYER
    self._type = type
    sprites = self._define_sprites()
    layers = self._define_layers()

    super().__init__(sprites, x, y, order_in_layer, layers, min_x, max_x, min_y, max_y)
    self._sprites = sprites

  @GameObject._start_decorator
  def start(self) -> None:
    self._component_manager.add(SpriteRendererComponent, self)
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