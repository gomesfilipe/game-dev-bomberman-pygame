from abc import ABC, abstractmethod
import pygame
from typing import Tuple

class Sprites(ABC):
  @abstractmethod
  def initialize_sprites(self) -> None:
    pass

  def _read_sprite(self, path: str, size: Tuple[int, int]) -> pygame.Surface:
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, size)
    image = image.convert_alpha()
    return image