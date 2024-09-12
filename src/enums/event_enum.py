from enum import Enum
# from src.game_objects.game_object import GameObject
import pygame
from typing import Dict, Callable

class EventEnum(Enum):
  COLLISION = pygame.USEREVENT + 1
  NEW_GAME_OBJECT = pygame.USEREVENT + 2
  DESTROY_GAME_OBJECT = pygame.USEREVENT + 3
  QUIT = pygame.QUIT
  PRESSED_KEY = pygame.KEYDOWN

  def post_event(self, **kwargs) -> None:
    post_handlers: Dict[EventEnum, Callable] = {
      EventEnum.NEW_GAME_OBJECT: lambda: self.__post_new_game_object_event(**kwargs),
      EventEnum.DESTROY_GAME_OBJECT: lambda: self.__post_destroy_game_object_event(**kwargs),
    }

    if self in post_handlers:
      post_handlers[self]()
    else:
      self.__post_default_event()

  @classmethod
  def __post_new_game_object_event(cls, game_object) -> None:
    pygame.event.post(pygame.event.Event(cls.NEW_GAME_OBJECT.value, game_object = game_object))

  @classmethod
  def __post_destroy_game_object_event(cls, game_object) -> None:
    pygame.event.post(pygame.event.Event(cls.DESTROY_GAME_OBJECT.value, game_object = game_object))

  def __post_default_event(self) -> None:
    pygame.event.post(pygame.event.Event(self.value))