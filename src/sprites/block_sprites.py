from src.sprites.sprites import Sprites
from typing import Tuple
import pygame

class BlockSprites(Sprites):
  def __init__(self, idle_path, size: Tuple[int, int]) -> None:
    self.__idle_path = idle_path
    self.__size = size

  def initialize_sprites(self) -> None:
    self.__idle = self._read_sprite(self.__idle_path, self.__size)

  def idle(self) -> pygame.Surface:
    return self.__idle
