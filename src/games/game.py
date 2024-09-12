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
      game_objects: List[GameObject],
      observers: List[ObserverInterface] = [],
    ) -> None:
    self._scene = scene
    self._game_objects: List[GameObject] = game_objects
    self._observers = observers + [self]
    self._stop: bool = False

    self._x: Optional[float] = None
    self._y: Optional[float] = None

    self._time_to_sort_game_objects: float = 0.5
    self._time_last_sort: float = time.time()

    self._collider_groups = self._build_collider_groups()

  def _build_collider_groups(self) -> Dict[str, List[GameObject]]:
    collider_groups: Dict[str, List[GameObject]] = {}

    for game_object in self._game_objects:
      for layer in game_object.get_layers():
        if layer in collider_groups:
          collider_groups[layer].append(game_object)
        else:
          collider_groups[layer] = [game_object]

    return collider_groups

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
      pygame.K_SPACE: lambda: self.__switch_debug_mode(),
    }

    if event.key in keys:
      keys[event.key]()

  def __handle_new_game_object_event(self, event: pygame.event.Event) -> None:
    self.__add_game_object(event.game_object)

  def __handle_destroy_game_object_event(self, event: pygame.event.Event) -> None:
    self.__delete_game_object(event.game_object)

  def __switch_debug_mode(self) -> None:
    for game_object in self._game_objects:
      game_object.switch_debug_mode()

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
      self.__update_game_objects()
      self.__handle_collisions()
      self.__update_scenes()

    pygame.quit()

  def __start(self) -> None:
    pygame.init()
    self._scene.start_scene()

    for game_object in self._game_objects:
      game_object.start()

  def __handle_events(self) -> None:
    for event in pygame.event.get():
      self._handle_event(event)

  def __update_game_objects(self) -> None:
    for game_object in self._game_objects:
      game_object.update()

  def __handle_collisions(self) -> None:
    for layer, colliders in self._collider_groups.items():
      for i in range(len(colliders)):
        for j in range(i + 1, len(colliders)):
          if colliders[i].is_colliding(colliders[j]):
            colliders[i].on_collide(colliders[j], layer)
            colliders[j].on_collide(colliders[i], layer)
            EventEnum.COLLISION.post_event()

  def __update_scenes(self) -> None:
    now = time.time()

    # Reordena os GabeObjects baseados na sua order in layer num certo intervalo de tempo.
    if now >= self._time_last_sort + self._time_to_sort_game_objects:
      self.__sort_game_objects_by_order_in_layer()
      self._time_last_sort = now

    self._scene.get_screen().fill('wheat3')
    self._scene.update_scene()

    for game_object in self._game_objects:
      game_object.update_scene()

    pygame.display.flip()

  def __sort_game_objects_by_order_in_layer(self) -> None:
    key_func: Callable[[GameObject], Tuple[int, int]] = lambda game_object: (game_object.get_order_in_layer(), random.random())
    self._game_objects.sort(key = key_func)

  def __delete_game_object(self, game_object: GameObject) -> None:
    layers = game_object.get_layers()

    for layer in layers:
      self._collider_groups[layer].remove(game_object)

    self._game_objects.remove(game_object)

  def __add_game_object(self, game_object: GameObject) -> None:
    layers = game_object.get_layers()

    for layer in layers:
      if layer in layers:
        self._collider_groups[layer].append(game_object)
      else:
        self._collider_groups[layer] = [game_object]

    self._game_objects.append(game_object)
    self.__sort_game_objects_by_order_in_layer()
