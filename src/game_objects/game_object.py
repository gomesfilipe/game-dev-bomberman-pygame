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
      layers: List[str] = [],
      debug: bool = False,
  ) -> None:
    self._sprites = sprites
    self._scene = scene
    self._layers = layers
    self._x = x
    self._y = y
    self._debug = debug

    self._current_sprite: Optional[pygame.Surface] = None
    self._images: Dict[str, pygame.Surface] = {}

  def _start_decorator(func: Callable) -> Callable:
    def initialize_sprites(self: 'GameObject') -> None:
      self._sprites.initialize_sprites()
      func(self)

    return initialize_sprites

  def _update_scene_decorator(func: Callable) -> Callable:
    def show_hitbox(self: 'GameObject') -> None:
      func(self)

      if self._debug:
        screen = self._scene.get_screen()
        pygame.draw.rect(screen, (255, 0, 0), self._current_sprite.get_rect(x = self._x, y = self._y), 2)

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

  def _valid_position(self, x: float, y: float) -> bool:
    screen = self._scene.get_screen()
    display = self._scene.get_display()

    return x > 0 and x + self._current_sprite.get_width() < screen.get_width() and \
      y > display.height() and y + self._current_sprite.get_height() < screen.get_height()

  def get_layers(self) -> List[str]:
    return self._layers

  def is_colliding(self, other: 'GameObject') -> bool:
    self_rect = self._current_sprite.get_rect(x = self._x, y = self._y)
    other_rect = other._current_sprite.get_rect(x = other._x, y = other._y)

    return self_rect.colliderect(other_rect)
