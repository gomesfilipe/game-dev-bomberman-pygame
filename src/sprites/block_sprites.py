from src.core.sprites import Sprites
from typing import Tuple
import pygame

class SimpleSprite(Sprites):
  def __init__(self, idle_path, size: Tuple[int, int]) -> None:
    super().__init__(size)
    self.__idle_path = idle_path

  def initialize_sprites(self) -> None:
    self.__idle = self._read_sprite(self.__idle_path)

  def idle(self) -> pygame.Surface:
    return self.__idle
