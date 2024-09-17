from typing import List, Tuple, Dict, Optional
from src.enums.direction_enum import DirectionEnum
from src.core.game_object import GameObject
from src.sprites.block_sprites import SimpleSprite
from src.components.sprite_renderer_component import SpriteRendererComponent
from src.components.movement_controller_component import MovementControllerComponent
from src.game_objects.explosion_game_object import ExplosionGameObject
from config import EXPLOSION_ORDER_IN_LAYER, BOMB_SPRITE
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
      super_bomb: bool = False,
      layers: List[str] = [],
      min_x: float = -float('inf'),
      max_x: float = float('inf'),
      min_y: float = -float('inf'),
      max_y: float = float('inf'),
    ) -> None:
    self._size = size
    sprites =  BOMB_SPRITE

    super().__init__(sprites, x, y, order_in_layer, layers, min_x, max_x, min_y, max_y)
    self._sprites = sprites
    self._explosion_time = explosion_time
    self._explosion_range = explosion_range
    self._kick_range = kick_range
    self._super_bomb = super_bomb

  @GameObject._start_decorator
  def start(self) -> None:
    self._component_manager.add(SpriteRendererComponent, self)
    self._current_sprite: pygame.Surface = self._sprites.idle()
    self._start_time: float = time.time()

  @GameObject._update_decorator
  def update(self) -> None:
    if not self.__should_explode():
      return

    width = self._sprites._hitbox.get_width()
    height = self._sprites._hitbox.get_height()

    positions: Dict[DirectionEnum, Tuple[int, int]] = {
      DirectionEnum.UP: (self._x, self._y - height),
      DirectionEnum.LEFT: (self._x - width, self._y),
      DirectionEnum.DOWN: (self._x, self._y + height),
      DirectionEnum.RIGHT: (self._x + width, self._y),
      None: (self._x, self._y),
    }

    for direction, position in positions.items():
      x, y = position

      if not self._valid_position(x, y):
        continue

      self.instantiate(
        ExplosionGameObject,
        x = x,
        y = y,
        size = self._size,
        order_in_layer = EXPLOSION_ORDER_IN_LAYER,
        explosion_range = self._explosion_range - 1,
        directions = self.__define_directions(direction),
        layers = ['player1_explosion', 'player2_explosion', 'explosion'],
        min_x = self._min_x,
        max_x = self._max_x,
        min_y = self._min_y,
        max_y = self._max_y,
      )

    self.destroy()

  def on_collide(self, other: GameObject, layer: str) -> None:
    return

  def __should_explode(self) -> bool:
    return time.time() - self._start_time >= self._explosion_time

  def __define_directions(self, direction: Optional[DirectionEnum]) -> List[DirectionEnum]:
    if direction is None:
      return []

    if self._super_bomb:
      return DirectionEnum.cases()

    return [direction]