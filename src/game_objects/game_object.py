from abc import ABC, abstractmethod
from typing import Dict, Tuple, Optional, Callable, List
from src.scenes.scene import Scene
from src.utils.player_commands import PlayerCommands
from src.sprites.player_sprites import PlayerSprites
import pygame

class GameObject(ABC):
  def __init__(
      self,
      sprites: PlayerSprites,
      scene: Scene,
      commands: PlayerCommands,
      layers: List[str] = [],
  ) -> None:
    self._sprites = sprites
    self._scene = scene
    self._commands = commands
    self._layers = layers

    self._x: Optional[float] = None
    self._y: Optional[float] = None

    self._current_image: Optional[pygame.Surface] = None
    self._images: Dict[str, pygame.Surface] = {}

  def _start_decorator(func: Callable) -> Callable:
    def initialize_sprites(self: 'GameObject') -> None:
      self._sprites.initialize_sprites()
      func(self)

    return initialize_sprites

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

    return x > 0 and x + self._current_image.get_width() < screen.get_width() and \
      y > display.height() and y + self._current_image.get_height() < screen.get_height()

  def get_layers(self) -> List[str]:
    return self._layers

  def is_colliding(self, other: 'GameObject') -> bool:
    self_rect = self._current_image.get_rect(x = self._x, y = self._y)
    other_rect = other._current_image.get_rect(x = other._x, y = other._y)

    return self_rect.colliderect(other_rect)
