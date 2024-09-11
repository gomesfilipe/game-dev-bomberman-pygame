from abc import ABC, abstractmethod
import pygame
from typing import Tuple

class Sprites(ABC):
  def __init__(self, size: Tuple[int, int]) -> None:
    self._size = size

  @abstractmethod
  def initialize_sprites(self) -> None:
    pass

  # TODO
  def initialize_hitbox(self) -> None:
    pass

  def _read_sprite(self, path: str) -> pygame.Surface:
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, self._size)
    image = image.convert_alpha()
    return image

  def width(self) -> int:
    return self._size[0]

  def height(self) -> int:
    return self._size[1]