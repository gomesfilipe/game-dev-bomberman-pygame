from typing import List
from src.game_objects.game_object import GameObject
from src.sprites.block_sprites import SimpleSprite
from src.scenes.scene import Scene
import pygame

class BlockGameObject(GameObject):
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
    self._sprites = sprites

  @GameObject._start_decorator
  def start(self) -> None:
    self._current_sprite: pygame.Surface = self._sprites.idle()

  def update(self) -> None:
    return

  def on_collide(self, other: GameObject, layer: str) -> None:
    return
