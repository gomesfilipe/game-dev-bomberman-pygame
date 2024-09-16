from src.core.sprites import Sprites
from typing import Tuple
import pygame

class PlayerSprites(Sprites):
  def __init__(
      self,
      up_path: str,
      left_path: str,
      down_path: str,
      right_path: str,
      face_path: str,
      left_dead_path: str,
      right_dead_path: str,
      size: Tuple[int, int]
  ) -> None:
    super().__init__(size)

    self.__up_path = up_path
    self.__left_path = left_path
    self.__down_path = down_path
    self.__right_path = right_path
    self.__face_path = face_path
    self.__left_dead_path = left_dead_path
    self.__right_dead_path = right_dead_path

  def initialize_sprites(self) -> None:
    self.__up = self._read_sprite(self.__up_path)
    self.__left = self._read_sprite(self.__left_path)
    self.__down = self._read_sprite(self.__down_path)
    self.__right = self._read_sprite(self.__right_path)
    self.__face = self._read_sprite(self.__face_path)
    self.__left_dead = self._read_sprite(self.__left_dead_path)
    self.__right_dead = self._read_sprite(self.__right_dead_path)

  def initialize_hitbox(self) -> None:
    self._hitbox = pygame.Surface((self._size[0] / 2, self._size[1] / 2))

  def sprites_position(self, x: float, y: float) -> Tuple[float, float]:
    return x - self.width() / 4, y - self.height() / 2

  def up(self) -> pygame.Surface:
    return self.__up

  def left(self) -> pygame.Surface:
    return self.__left

  def down(self) -> pygame.Surface:
    return self.__down

  def right(self) -> pygame.Surface:
    return self.__right

  def face(self) -> pygame.Surface:
    return self.__face

  def left_dead(self) -> pygame.Surface:
    return self.__left_dead

  def right_dead(self) -> pygame.Surface:
    return self.__right_dead
