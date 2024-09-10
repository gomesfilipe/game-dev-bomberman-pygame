from src.displays.display import Display
from typing import List, Optional
import pygame
import time
from src.enums.event_enum import EventEnum
from src.utils.utils import format_seconds_to_min_sec
from src.sprites.player_sprites import PlayerSprites

class ScoreDisplay(Display):
  def __init__(
    self,
    screen: pygame.Surface,
    duration: int,
    max_lives: int,
    player1_sprites: PlayerSprites,
    player2_sprites: PlayerSprites,
  ) -> None:
    super().__init__(screen)

    self._duration = duration
    self._max_lives = max_lives
    self._player1_sprites = player1_sprites
    self._player2_sprites = player2_sprites

  def start(self) -> None:
    self._time_spent: int = 0
    self._player1_lives = self._max_lives
    self._player2_lives = self._max_lives

    self._player1_sprites.initialize_sprites()
    self._player2_sprites.initialize_sprites()

    self._font: pygame.font.Font = pygame.font.SysFont('impact', 48)
    self._start_time: int = int(time.time())
    self._remaining_time: int = self._duration

  def update(self) -> None:
    self.__update_background_rect()
    self.__update_player1_image()
    self.__update_player2_image()
    self.__update_remainig_time()
    self.__update_player1_lives()
    self.__update_player2_lives()

  def height(self) -> float:
    return 80.0

  def width(self) -> float:
    return self._screen.get_width()

  def handle_event(self, event: int) -> None:
    handlers = {
      EventEnum.COLLISION.value: self.__handle_colision_event
    }

    handlers[event]()

  def __handle_colision_event(self) -> None:
    self._score += 1

  def interested_events(self) -> List[int]:
    return [EventEnum.COLLISION.value]

  def __update_background_rect(self) -> None:
    pygame.draw.rect(self._screen, 'black', (0, 0, self.width(), self.height()))

  def __update_player1_image(self) -> None:
    player1_image = self._player1_sprites.face()
    x = (self.height() - player1_image.get_height()) / 2
    self._screen.blit(player1_image, (x, x))

  def __update_player2_image(self) -> None:
    player2_image = self._player2_sprites.face()
    y = (self.height() - player2_image.get_height()) / 2
    x = self.width() - y - player2_image.get_width()
    self._screen.blit(player2_image, (x, y))

  def __update_remainig_time(self) -> None:
    self._time_spent = int(time.time() - self._start_time)
    self._remaining_time = max(self._duration - self._time_spent, 0)

    remaining_time_image = self._font.render(f'{format_seconds_to_min_sec(self._remaining_time)}', True, (255, 255, 255))
    x = (self.width() - remaining_time_image.get_width()) / 2
    y = (self.height() - remaining_time_image.get_height()) / 2
    self._screen.blit(remaining_time_image, (x, y))

  def __update_player1_lives(self) -> None:
    player1_lives_image = self._font.render(str(self._player1_lives), True, (255, 255, 255))
    x = self.height()
    y = (self.height() - player1_lives_image.get_height()) / 2
    self._screen.blit(player1_lives_image, (x, y))

  def __update_player2_lives(self) -> None:
    player2_lives_image = self._font.render(str(self._player2_lives), True, (255, 255, 255))
    x = self.width() - self.height() - player2_lives_image.get_width()
    y = (self.height() - player2_lives_image.get_height()) / 2
    self._screen.blit(player2_lives_image, (x, y))