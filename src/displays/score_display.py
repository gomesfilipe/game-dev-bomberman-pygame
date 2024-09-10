from src.displays.display import Display
from typing import List, Optional
import pygame
import time
from src.interfaces.observer_interface import ObserverInterface
from src.enums.event_enum import EventEnum

class ScoreDisplay(Display, ObserverInterface):
  def __init__(self, screen: pygame.Surface) -> None:
    super().__init__(screen)

    self._time_spent: Optional[int] = None
    self._score: Optional[int] = None
    self._font: Optional[pygame.font.Font] = None
    self._start_time: Optional[pygame.font.Font] = None

  def start(self) -> None:
    self._time_spent = 0
    self._score = 0
    self._font = pygame.font.SysFont('impact', 48)
    self._start_time = int(time.time())

  def update(self) -> None:
    self._time_spent = int(time.time() - self._start_time)
    time_spent_image = self._font.render(f'Time Spent: {self._time_spent}', True, (255, 255, 255))
    score_image = self._font.render(f'Score: {self._score}', True, (255, 255, 255))

    pygame.draw.rect(self._screen, 'blue', (0, 0, self._screen.get_width(), self.height()))
    self._screen.blit(time_spent_image, (0, 0))
    self._screen.blit(score_image, (self._screen.get_width() - score_image.get_width(), 0))

  def height(self) -> float:
    return 35.0

  def handle_event(self, event: int) -> None:
    handlers = {
      EventEnum.COLLISION.value: self.__handle_colision_event
    }

    handlers[event]()

  def __handle_colision_event(self) -> None:
    self._score += 1

  def interested_events(self) -> List[int]:
    return [EventEnum.COLLISION.value]
