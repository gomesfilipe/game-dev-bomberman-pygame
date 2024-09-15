from typing import List, Tuple
from src.core.game_object import GameObject
from src.sprites.block_sprites import SimpleSprite
from src.components.sprite_renderer_component import SpriteRendererComponent
from src.components.movement_controller_component import MovementControllerComponent
import pygame
import time
from os.path import join

class BombGameObject(GameObject):
  def __init__(
      self,
      x: float,
      y: float,
      size: Tuple[int, int],
      order_in_layer: int,
      explosion_time: int,
      explosion_range: int,
      kick_range: int,
      layers: List[str] = [],
      min_x: float = -float('inf'),
      max_x: float = float('inf'),
      min_y: float = -float('inf'),
      max_y: float = float('inf'),
    ) -> None:
    self._size = size
    sprites =  SimpleSprite(join('assets', 'bomb', 'bomb.png'), self._size)

    super().__init__(sprites, x, y, order_in_layer, layers, min_x, max_x, min_y, max_y)
    self._sprites = sprites
    self._explosion_time = explosion_time
    self._explosion_range = explosion_range
    self._kick_range = kick_range

  @GameObject._start_decorator
  def start(self) -> None:
    self._component_manager.add(SpriteRendererComponent, self)
    self._current_sprite: pygame.Surface = self._sprites.idle()
    self._start_time: float = time.time()

  @GameObject._update_decorator
  def update(self) -> None:
    if self.__should_explode():
      self.destroy()

  def on_collide(self, other: GameObject, layer: str) -> None:
    return

  def __should_explode(self) -> bool:
    return time.time() - self._start_time >= self._explosion_time
