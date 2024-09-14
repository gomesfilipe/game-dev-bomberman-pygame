
from src.core.base_object import BaseObject
from typing import List, Type, Dict, Callable, Tuple
from src.core.game_object import GameObject
from src.enums.event_enum import EventEnum
import random
import time
import pygame

class GameObjectManager(BaseObject):
  def __init__(self):
    self._game_objects: List[GameObject] = []
    self._collider_groups = self._build_collider_groups()

    self._time_to_sort_game_objects: float = 0.5
    self._time_last_sort: float = time.time()

  def add(self, game_object: GameObject):
    layers = game_object.get_layers()

    for layer in layers:
      if layer in self._collider_groups:
        self._collider_groups[layer].append(game_object)
      else:
        self._collider_groups[layer] = [game_object]

    self._game_objects.append(game_object)
    self.__sort_game_objects_by_order_in_layer()

  def remove(self, game_object: GameObject):
    layers = game_object.get_layers()

    for layer in layers:
      if game_object in self._collider_groups[layer]:
        self._collider_groups[layer].remove(game_object)

    if game_object in self._game_objects:
      self._game_objects.remove(game_object)

  def get(self, game_object_class: Type[GameObject]):
    for game_object in self._game_objects:
      if isinstance(game_object, game_object_class):
          return game_object

    return None

  def start(self):
    for game_object in self._game_objects:
      game_object.start()

  def update(self):
    now = time.time()

    # Reordena os GameObjects baseados na sua order in layer num certo intervalo de tempo.
    if now >= self._time_last_sort + self._time_to_sort_game_objects:
      self.__sort_game_objects_by_order_in_layer()
      self._time_last_sort = now

    for game_object in self._game_objects:
      game_object.update()

    self.__handle_collisions()

  def fixed_update(self) -> None:
    for game_object in self._game_objects:
      game_object.fixed_update()

  def draw(self, screen: pygame.Surface) -> None:
    for game_object in self._game_objects:
      game_object.draw(screen)

  def _build_collider_groups(self) -> Dict[str, List[GameObject]]:
    collider_groups: Dict[str, List[GameObject]] = {}

    for game_object in self._game_objects:
      for layer in game_object.get_layers():
        if layer in collider_groups:
          collider_groups[layer].append(game_object)
        else:
          collider_groups[layer] = [game_object]

    return collider_groups

  def __handle_collisions(self) -> None:
    for layer, colliders in self._collider_groups.items():
      for i in range(len(colliders)):
        for j in range(i + 1, len(colliders)):
          if colliders[i].is_colliding(colliders[j]):
            colliders[i].on_collide(colliders[j], layer)
            colliders[j].on_collide(colliders[i], layer)
            EventEnum.COLLISION.post_event()

  def switch_debug_mode(self) -> None:
    for game_object in self._game_objects:
      game_object.switch_debug_mode()

  def __sort_game_objects_by_order_in_layer(self) -> None:
    key_func: Callable[[GameObject], Tuple[int, int]] = lambda game_object: (game_object.get_order_in_layer(), random.random())
    self._game_objects.sort(key = key_func)
