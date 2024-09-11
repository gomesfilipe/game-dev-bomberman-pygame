from abc import ABC, abstractmethod
from typing import Dict, Tuple, Optional, Callable, List
from src.scenes.scene import Scene
from src.utils.player_commands import PlayerCommands
from src.sprites.sprites import Sprites
import pygame

class GameObject(ABC):
  def __init__(
      self,
      sprites: Sprites,
      scene: Scene,
      x: float,
      y: float,
      order_in_layer: int,
      layers: List[str] = [],
  ) -> None:
    self._sprites = sprites
    self._scene = scene
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

  def _update_scene_decorator(func: Callable) -> Callable:
    def show_hitbox(self: 'GameObject') -> None:
      func(self)

      if self._debug:
        sprite_x, sprite_y = self._sprites.sprites_position(self._x, self._y)
        screen = self._scene.get_screen()
        pygame.draw.rect(screen, 'blue', self._current_sprite.get_rect(x = sprite_x, y = sprite_y), 2)
        pygame.draw.rect(screen, (255, 0, 0), self._sprites._hitbox.get_rect(x = self._x, y = self._y), 2)

    return show_hitbox

  @abstractmethod
  def start(self) -> None:
    pass

  @abstractmethod
  def update(self) -> None:
    pass

  @abstractmethod
  def update_scene(self) -> None:
    pass

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
