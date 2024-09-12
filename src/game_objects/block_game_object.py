from typing import List
from src.game_objects.game_object import GameObject
from src.sprites.block_sprites import BlockSprites
from src.scenes.scene import Scene
import pygame

class BlockGameObject(GameObject):
  def __init__(
      self,
      sprites: BlockSprites,
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

  @GameObject._update_scene_decorator
  def update_scene(self) -> None:
    screen = self._scene.get_screen()
    screen.blit(self._current_sprite, (self._x, self._y))

  def on_collide(self, other: GameObject, layer: str) -> None:
    return
