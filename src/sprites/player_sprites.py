from src.sprites.sprites import Sprites
from typing import Tuple
import pygame

class PlayerSprites(Sprites):
  def __init__(self, up_path: str, left_path: str, down_path: str, right_path: str, size: Tuple[int, int]) -> None:
    self.__up_path = up_path
    self.__left_path = left_path
    self.__down_path = down_path
    self.__right_path = right_path
    self.__size = size

  def initialize_sprites(self) -> None:
    self.__up = self._read_sprite(self.__up_path, self.__size)
    self.__left = self._read_sprite(self.__left_path, self.__size)
    self.__down = self._read_sprite(self.__down_path, self.__size)
    self.__right = self._read_sprite(self.__right_path, self.__size)

  def up(self) -> pygame.Surface:
    return self.__up

  def left(self) -> pygame.Surface:
    return self.__left

  def down(self) -> pygame.Surface:
    return self.__down

  def right(self) -> pygame.Surface:
    return self.__right
