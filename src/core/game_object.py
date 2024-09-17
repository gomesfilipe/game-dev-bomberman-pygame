from src.core.base_object import BaseObject

class GameObject(BaseObject):
  pass

from abc import abstractmethod
from typing import Dict, Tuple, Optional, Callable, List, Type, Any
from src.enums.event_enum import EventEnum
from src.core.sprites import Sprites
from src.core.component_manager import ComponentManager
from src.core.component import Component
from src.commands.movement_commands import MovementCommands
from src.commands.skill_commands import SkillCommands
from src.enums.direction_enum import DirectionEnum
from src.utils.utils import between
import pygame

class GameObject(BaseObject):
  def __init__(
      self,
      sprites: Sprites,
      x: float,
      y: float,
      order_in_layer: int,
      layers: List[str] = [],
      min_x: float = -float('inf'),
      max_x: float = float('inf'),
      min_y: float = -float('inf'),
      max_y: float = float('inf'),
  ) -> None:
    self._sprites = sprites
    self._order_in_layer = order_in_layer
    self._layers = layers
    self._debug = False
    self._movement_commands: Optional[MovementCommands] = None
    self._skill_commands: Optional[SkillCommands] = None

    self._min_x = min_x
    self._max_x = max_x
    self._min_y = min_y
    self._max_y = max_y
    self._x = x
    self._y = y
    self._theta: float = 0.0
    self._previous_x = self._x
    self._previous_y = self._y
    self._velocity: float = 0.0
    self._vx: float = 0.0
    self._vy: float = 0.0
    self._direction: DirectionEnum = DirectionEnum.DOWN

    self._component_manager = ComponentManager(self)
    self._current_sprite: Optional[pygame.Surface] = None
    self._images: Dict[str, pygame.Surface] = {}

  def _start_decorator(func: Callable) -> Callable:
    def initialize_sprites(self: 'GameObject') -> None:
      # self._sprites.initialize_sprites()
      # self._sprites.initialize_hitbox()
      func(self)

    return initialize_sprites

  def _update_decorator(func: Callable) -> None:
    def update_components(self: 'GameObject') -> None:
      self._component_manager.update()
      func(self)

    return update_components

  def draw(self, screen: pygame.Surface) -> None:
    self._component_manager.draw(screen)

  def _show_hitbox(self, screen: pygame.Surface) -> None:
    sprite_x, sprite_y = self._sprites.sprites_position(self._x, self._y)
    pygame.draw.rect(screen, 'blue', self._current_sprite.get_rect(x = sprite_x, y = sprite_y), 2)
    pygame.draw.rect(screen, (255, 0, 0), self._sprites._hitbox.get_rect(x = self._x, y = self._y), 2)

  @abstractmethod
  def on_collide(self, other: 'GameObject', layer: str) -> None:
    pass

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

  def get_component(self, component_class: Type[Component]) -> Optional[Component]:
    return self._component_manager.get(component_class)

  def _valid_position(self, x: float, y: float) -> bool:
    width = self._sprites._hitbox.get_width()
    height = self._sprites._hitbox.get_height()

    return between(x, self._min_x, self._max_x - width) and \
      between(y, self._min_y, self._max_y - height)
