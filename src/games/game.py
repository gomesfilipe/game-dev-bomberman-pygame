import pygame
from typing import Tuple, Optional, List, Dict, Callable
from abc import ABC, abstractmethod
from src.game_objects.game_object import GameObject
from src.scenes.scene import Scene
from src.interfaces.observer_interface import ObserverInterface
from src.enums.event_enum import EventEnum
import random
import time

class Game(ObserverInterface):
  def __init__(
      self,
      scene: Scene,
      observers: List[ObserverInterface] = [],
    ) -> None:
    self._scene = scene
    self._observers = observers + [self]
    self._stop: bool = False

    self._x: Optional[float] = None
    self._y: Optional[float] = None

  def _should_stop(self) -> None:
    return self._stop

  def handle_event(self, event: pygame.event.Event) -> None:
    handlers: Dict[int, Callable] = {
      EventEnum.QUIT.value: lambda: self.__handle_quit_event(event),
      EventEnum.PRESSED_KEY.value: lambda: self.__handle_pressed_key_event(event),
      EventEnum.NEW_GAME_OBJECT.value: lambda: self.__handle_new_game_object_event(event),
      EventEnum.DESTROY_GAME_OBJECT.value: lambda: self.__handle_destroy_game_object_event(event),
    }

    handlers[event.type]()

  def __handle_quit_event(self, event: pygame.event.Event) -> None:
    self._stop = True

  def __handle_pressed_key_event(self, event: pygame.event.Event) -> None:
    keys: Dict[int, Callable] = {
      pygame.K_SPACE: lambda: self._scene.switch_debug_mode(),
    }

    if event.key in keys:
      keys[event.key]()

  def __handle_new_game_object_event(self, event: pygame.event.Event) -> None:
    self._scene.add_game_object(event.game_object)

  def __handle_destroy_game_object_event(self, event: pygame.event.Event) -> None:
    self._scene.remove_game_object(event.game_object)

  def interested_events(self) -> List[int]:
    return [
      EventEnum.QUIT.value,
      EventEnum.PRESSED_KEY.value,
      EventEnum.NEW_GAME_OBJECT.value,
      EventEnum.DESTROY_GAME_OBJECT.value,
    ]

  def _handle_event(self, event: pygame.event.Event) -> None:
    for observer in self._observers:
      if event.type in observer.interested_events():
        observer.handle_event(event)

  def run(self):
    self.__start()

    while not self._should_stop():
      self.__handle_events()
      self.__update_scenes()

    pygame.quit()

  def __start(self) -> None:
    pygame.init()
    self._scene.start_scene()

  def __handle_events(self) -> None:
    for event in pygame.event.get():
      self._handle_event(event)

  def __update_scenes(self) -> None:
    self._scene.get_screen().fill('wheat3')
    self._scene.update_scene()

    pygame.display.flip()
