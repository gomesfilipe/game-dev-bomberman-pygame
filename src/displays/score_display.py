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

    self._font: pygame.font.Font = pygame.font.SysFont('impact', 40)
    self._start_time: int = int(time.time())
    self._remaining_time: int = self._duration

  def update(self) -> None:
    self._time_spent = int(time.time() - self._start_time)
    self._remaining_time = max(self._duration - self._time_spent, 0)

    player1_image = self._player1_sprites.face()
    player2_image = self._player2_sprites.face()

    score_image = self._font.render(f'{self._player1_lives} X {self._player2_lives}', True, (255, 255, 255))
    remaining_time_image = self._font.render(f'{format_seconds_to_min_sec(self._remaining_time)}', True, (255, 255, 255))

    pygame.draw.rect(self._screen, 'blue', (0, 0, self._screen.get_width(), self.height()))
    self._screen.blit(player1_image, (200, 0))
    self._screen.blit(player2_image, (300, 0))
    self._screen.blit(score_image, (0, 0))
    self._screen.blit(remaining_time_image, (self._screen.get_width() - remaining_time_image.get_width(), 0))

  def height(self) -> float:
    return 65.0

  def handle_event(self, event: int) -> None:
    handlers = {
      EventEnum.COLLISION.value: self.__handle_colision_event
    }

    handlers[event]()

  def __handle_colision_event(self) -> None:
    self._score += 1

  def interested_events(self) -> List[int]:
    return [EventEnum.COLLISION.value]
