from src.core.display import Display
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
    player1_name: str,
    player2_name: str,
  ) -> None:
    super().__init__(screen)

    self._duration = duration
    self._max_lives = max_lives
    self._player1_sprites = player1_sprites
    self._player2_sprites = player2_sprites
    self._player1_name = player1_name
    self._player2_name = player2_name

  def start(self) -> None:
    self._time_spent: int = 0
    self._player1_lives = self._max_lives
    self._player2_lives = self._max_lives

    self._player1_sprites.initialize_sprites()
    self._player2_sprites.initialize_sprites()

    self._font: pygame.font.Font = pygame.font.SysFont('impact', 48)
    self._start_time: int = int(time.time())
    self._remaining_time: int = self._duration

  def draw(self, screen: pygame.Surface) -> None:
    self.__draw_background_rect(screen)
    self.__draw_player1_image(screen)
    self.__draw_player2_image(screen)
    self.__draw_remainig_time(screen)
    self.__draw_player1_lives(screen)
    self.__draw_player2_lives(screen)

  def height(self) -> float:
    return 80.0

  def handle_event(self, event: pygame.event.Event) -> None:
    handlers = {
      EventEnum.LIFE_POWER_COLLECTED.value: lambda: self.__handle_life_power_collected_event(event),
      EventEnum.SKULL_POWER_COLLECTED.value: lambda: self.__handle_skull_power_collected_event(event),
    }

    handlers[event.type]()

  def __handle_life_power_collected_event(self, event: pygame.event.Event) -> None:
    if self._player1_name == event.player_name:
      self._player1_lives += 1
    elif self._player2_name == event.player_name:
      self._player2_lives += 1
    else:
      print('warning: inexistent player name in __handle_life_power_collected_event')

  def __handle_skull_power_collected_event(self, event: pygame.event.Event) -> None:
    if self._player1_name == event.player_name:
      self._player1_lives -= 1
    elif self._player2_name == event.player_name:
      self._player2_lives -= 1
    else:
      print('warning: inexistent player name in __handle_death_power_collected_event')

  def interested_events(self) -> List[int]:
    return [
      EventEnum.LIFE_POWER_COLLECTED.value,
      EventEnum.SKULL_POWER_COLLECTED.value,
    ]

  def __draw_background_rect(self, screen: pygame.Surface) -> None:
    pygame.draw.rect(screen, 'black', (0, 0, self.width(), self.height()))

  def __draw_player1_image(self, screen: pygame.Surface) -> None:
    player1_image = self._player1_sprites.face()
    x = (self.height() - player1_image.get_height()) / 2
    screen.blit(player1_image, (x, x))

  def __draw_player2_image(self, screen: pygame.Surface) -> None:
    player2_image = self._player2_sprites.face()
    y = (self.height() - player2_image.get_height()) / 2
    x = self.width() - y - player2_image.get_width()
    screen.blit(player2_image, (x, y))

  def __draw_remainig_time(self, screen: pygame.Surface) -> None:
    self._time_spent = int(time.time() - self._start_time)
    self._remaining_time = max(self._duration - self._time_spent, 0)

    remaining_time_image = self._font.render(f'{format_seconds_to_min_sec(self._remaining_time)}', True, (255, 255, 255))
    x = (self.width() - remaining_time_image.get_width()) / 2
    y = (self.height() - remaining_time_image.get_height()) / 2
    screen.blit(remaining_time_image, (x, y))

  def __draw_player1_lives(self, screen: pygame.Surface) -> None:
    player1_lives_image = self._font.render(str(self._player1_lives), True, (255, 255, 255))
    x = self.height()
    y = (self.height() - player1_lives_image.get_height()) / 2
    screen.blit(player1_lives_image, (x, y))

  def __draw_player2_lives(self, screen: pygame.Surface) -> None:
    player2_lives_image = self._font.render(str(self._player2_lives), True, (255, 255, 255))
    x = self.width() - self.height() - player2_lives_image.get_width()
    y = (self.height() - player2_lives_image.get_height()) / 2
    screen.blit(player2_lives_image, (x, y))
