from typing import List
from src.core.game_object import GameObject
from src.sprites.block_sprites import SimpleSprite
from src.core.display import Display
from src.components.sprite_renderer_component import SpriteRendererComponent
from src.components.movement_controller_component import MovementControllerComponent
import pygame

class BlockGameObject(GameObject):
  def __init__(
      self,
      screen: pygame.Surface,
      display: Display,
      sprites: SimpleSprite,
      x: float,
      y: float,
      order_in_layer: int,
      layers: List[str] = [],
    ) -> None:
    super().__init__(screen, display, sprites, x, y, order_in_layer, layers)
    self._sprites = sprites

  @GameObject._start_decorator
  def start(self) -> None:
    self._component_manager.add(SpriteRendererComponent, self)
    self._component_manager.add(MovementControllerComponent, self)
    self._current_sprite: pygame.Surface = self._sprites.idle()

  @GameObject._update_decorator
  def update(self) -> None:
    return

  def on_collide(self, other: GameObject, layer: str) -> None:
    return
