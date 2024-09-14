from src.core.base_object import BaseObject
from abc import abstractmethod
from typing import Dict, Tuple, Optional, Callable, List, Type, Any
from src.enums.event_enum import EventEnum
from src.core.sprites import Sprites
from src.core.display import Display
import pygame

class GameObject(BaseObject):
  def __init__(
      self,
      screen: pygame.Surface,
      display: Display,
      sprites: Sprites,
      x: float,
      y: float,
      order_in_layer: int,
      layers: List[str] = [],
  ) -> None:
    self._screen = screen
    self._display = display
    self._sprites = sprites
    self._order_in_layer = order_in_layer
    self._layers = layers
    self._x = x
    self._y = y
    self._debug = False

    self._current_sprite: Optional[pygame.Surface] = None
    self._images: Dict[str, pygame.Surface] = {}

  def _start_decorator(func: Callable) -> Callable:
    def initialize_sprites(self: 'GameObject') -> None:
      self._sprites.initialize_sprites()
      self._sprites.initialize_hitbox()
      func(self)

    return initialize_sprites

  def draw(self, screen: pygame.Surface) -> None:
    x, y = self._sprites.sprites_position(self._x, self._y)
    self._screen.blit(self._current_sprite, (x, y))

    if self._debug:
      self._show_hitbox()

  def _show_hitbox(self) -> None:
    sprite_x, sprite_y = self._sprites.sprites_position(self._x, self._y)
    pygame.draw.rect(self._screen, 'blue', self._current_sprite.get_rect(x = sprite_x, y = sprite_y), 2)
    pygame.draw.rect(self._screen, (255, 0, 0), self._sprites._hitbox.get_rect(x = self._x, y = self._y), 2)

  @abstractmethod
  def on_collide(self, other: 'GameObject', layer: str) -> None:
    pass

  def _read_image(self, path: str, size: Tuple[int, int]) -> pygame.Surface:
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, size)
    image = image.convert_alpha()
    return image

  def get_layers(self) -> List[str]:
    return self._layers

  def get_order_in_layer(self) -> int:
    return self._order_in_layer

  def is_colliding(self, other: 'GameObject') -> bool:
    self_rect = self._sprites._hitbox.get_rect(x = self._x, y = self._y)
    other_rect = other._sprites._hitbox.get_rect(x = other._x, y = other._y)

    return self_rect.colliderect(other_rect)

  def switch_debug_mode(self) -> None:
    self._debug = not self._debug

  def instantiate(self, game_object_class: Type['GameObject'], **params: Dict[str, Any]) -> 'GameObject':
    game_object = game_object_class(**params)
    game_object.start()
    game_object._debug = self._debug
    EventEnum.NEW_GAME_OBJECT.post_event(game_object = game_object)
    return game_object

  def destroy(self) -> None:
    EventEnum.DESTROY_GAME_OBJECT.post_event(game_object = self)

  def fixed_update(self) -> None:
    return
