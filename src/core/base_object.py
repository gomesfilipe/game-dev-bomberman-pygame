from abc import ABC, abstractmethod
import pygame

class BaseObject(ABC):
  def __init__(self, name: str = ''):
    self.name = name

  @abstractmethod
  def start(self) -> None:
    """ start function called before game loop """

  @abstractmethod
  def update(self) -> None:
    """ update function called once per frame """

  @abstractmethod
  def fixed_update(self) -> None:
    """ update function called once per physics update """

  @abstractmethod
  def draw(self, screen: pygame.Surface) -> None:
    """ function to draw the object """
