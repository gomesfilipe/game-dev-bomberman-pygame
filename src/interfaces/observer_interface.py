from abc import ABC, abstractmethod
from typing import List
import pygame

class ObserverInterface(ABC):
  @abstractmethod
  def handle_event(self, event: pygame.event.Event) -> None:
    pass

  @abstractmethod
  def interested_events(self) -> List[int]:
    pass
