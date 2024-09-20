from typing import List
from src.core.game_object import GameObject
from src.sprites.simple_sprite import SimpleSprite
from src.components.sprite_renderer_component import SpriteRendererComponent
from src.components.movement_controller_component import MovementControllerComponent
from src.enums.game_object_type_enum import GameObjectTypeEnum
import pygame

class BlockGameObject(GameObject):
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
    self._sprites = sprites

  def start(self) -> None:
    self._component_manager.add(SpriteRendererComponent, self)
    self._current_sprite: pygame.Surface = self._sprites.idle()

  @GameObject._update_decorator
  def update(self) -> None:
    return

  def on_collide(self, other: GameObject, layer: str) -> None:
    return
