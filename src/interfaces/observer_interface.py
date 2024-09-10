from abc import ABC, abstractmethod
from typing import List

class ObserverInterface(ABC):
  @abstractmethod
  def handle_event(self, event: int) -> None:
    pass

  @abstractmethod
  def interested_events(self) -> List[int]:
    pass
