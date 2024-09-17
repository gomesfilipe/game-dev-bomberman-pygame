from typing import List, Tuple, FrozenSet, Dict, Callable
from src.core.game_object import GameObject
from src.sprites.block_sprites import SimpleSprite
from src.components.sprite_renderer_component import SpriteRendererComponent
from src.enums.direction_enum import DirectionEnum
import pygame
import time
from os.path import join
from config import EXPLOSION_DURATION, EXPLOSION_ORDER_IN_LAYER

class ExplosionGameObject(GameObject):
  def __init__(
      self,
      x: float,
      y: float,
      size: Tuple[int, int],
      order_in_layer: int,
      explosion_range: int,
      directions: FrozenSet[DirectionEnum],
      layers: List[str] = [],
      min_x: float = -float('inf'),
      max_x: float = float('inf'),
      min_y: float = -float('inf'),
      max_y: float = float('inf'),
    ) -> None:
    self._size = size
    sprites = SimpleSprite(join('assets', 'explosion', 'explosion.png'), self._size)

    super().__init__(sprites, x, y, order_in_layer, layers, min_x, max_x, min_y, max_y)
    self._sprites = sprites
    self._explosion_range = explosion_range
    self._directions = directions
    self._duration = EXPLOSION_DURATION
    self._propagated: bool = False
    self._first_update: bool = True

  @GameObject._start_decorator
  def start(self) -> None:
    self._component_manager.add(SpriteRendererComponent, self)
    self._current_sprite: pygame.Surface = self._sprites.idle()
    self._start_time: float = time.time()

  @GameObject._update_decorator
  def update(self) -> None:
    if self.__should_destroy():
      self.destroy()
      return

    if self._propagated or self._explosion_range < 0:
      return

    if self._first_update:
      self._first_update = False
      return

    for direction in self._directions:
      x, y = self.__position_by_direction(direction)

      if not self._valid_position(x, y):
        continue

      self.instantiate(
        ExplosionGameObject,
        x = x,
        y = y,
        size = self._size,
        order_in_layer = EXPLOSION_ORDER_IN_LAYER,
        explosion_range = self._explosion_range - 1,
        directions = self._directions,
        layers = self._layers,
        min_x = self._min_x,
        max_x = self._max_x,
        min_y = self._min_y,
        max_y = self._max_y,
      )

    self._propagated = True

  def on_collide(self, other: GameObject, layer: str) -> None:
    handlers: Dict[str, Callable] = {
      'player1_explosion': lambda: self.__handle_player_explosion_layer(other),
      'player2_explosion': lambda: self.__handle_player_explosion_layer(other),
      'explosion': lambda: self.__handle_explosion_layer(other),
    }

    if layer in handlers:
      handlers[layer]()

  def __handle_explosion_layer(self, other: GameObject) -> None:
    self.destroy()

  def __handle_player_explosion_layer(self, other: GameObject) -> None:
    if isinstance(other, ExplosionGameObject):
      return

    other.take_damage()

  def __should_destroy(self) -> bool:
    return time.time() - self._start_time >= self._duration

  def __position_by_direction(self, direction: DirectionEnum) -> Tuple[float, float]:
    width = self._sprites._hitbox.get_width()
    height = self._sprites._hitbox.get_height()

    positions: Dict[DirectionEnum, Tuple[int, int]] = {
      DirectionEnum.UP: (self._x, self._y - height),
      DirectionEnum.LEFT: (self._x - width, self._y),
      DirectionEnum.DOWN: (self._x, self._y + height),
      DirectionEnum.RIGHT: (self._x + width, self._y),
    }

    return positions[direction]
