from src.core.component import Component

class SpriteRendererComponent(Component):
  pass

from src.core.game_object import GameObject
import pygame

class SpriteRendererComponent(Component):
  def __init__(self, game_object: GameObject, name: str = ''):
    super().__init__(game_object, name)

  def draw(self, screen: pygame.Surface):
    x, y = self._game_object._sprites.sprites_position(self._game_object._x, self._game_object._y)
    screen.blit(self._game_object._current_sprite, (x, y))

    if self._game_object._debug:
      self.__show_hitbox(screen)

  def __show_hitbox(self, screen: pygame.Surface) -> None:
    sprite_x, sprite_y = self._game_object._sprites.sprites_position(self._game_object._x, self._game_object._y)
    pygame.draw.rect(screen, 'blue', self._game_object._current_sprite.get_rect(x = sprite_x, y = sprite_y), 2)
    pygame.draw.rect(screen, (255, 0, 0), self._game_object._sprites._hitbox.get_rect(x = self._game_object._x, y = self._game_object._y), 2)

  def start(self) -> None:
    return

  def update(self) -> None:
    return

  def fixed_update(self) -> None:
    return
