
import pygame
from typing import List, Callable, Optional

class GameEvents:
  _events: List[pygame.event.Event] = []

  @staticmethod
  def update() -> None:
    GameEvents._events = pygame.event.get()

  @staticmethod
  def find(condition_fn: Callable[[pygame.event.Event], bool]) -> Optional[pygame.event.Event]:
    for event in GameEvents._events:
      if condition_fn(event):
        return event

    return None

  @staticmethod
  def get(condition_fn: Callable[[pygame.event.Event], bool]) -> List[pygame.event.Event]:
    return [event for event in GameEvents._events if condition_fn(event)]
