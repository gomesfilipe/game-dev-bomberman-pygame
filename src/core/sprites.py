from abc import ABC, abstractmethod
import pygame
from typing import Tuple

class Sprites(ABC):
  def __init__(self, size: Tuple[int, int]) -> None:
    self._size = size

  @abstractmethod
  def initialize_sprites(self) -> None:
    pass

  def initialize_hitbox(self) -> None:
    self._hitbox = pygame.Surface((self._size[0], self._size[1]))

  def sprites_position(self, x: float, y: float) -> Tuple[float, float]:
    return x, y

  def _read_sprite(self, path: str) -> pygame.Surface:
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, self._size)
    image = image.convert_alpha()
    return image

  def width(self) -> int:
    return self._size[0]

  def height(self) -> int:
    return self._size[1]