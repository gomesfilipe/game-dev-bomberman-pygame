
from src.core.base_object import BaseObject
from src.core.component import Component
from src.core.game_object import GameObject
import pygame
from typing import List, Type

class ComponentManager(BaseObject):
  def __init__(self, owner_game_object: GameObject):
    self._components: List[Component] = []
    self._owner_game_object = owner_game_object

  def add(self, component_class: Type[Component],  *args, **kwargs):
    self._components.append(component_class(self._owner_game_object, *args, **kwargs))

  def remove(self, component: Component):
    if component in self._components:
      self._components.remove(component)

  def get(self, component_class: Type[Component]):
    for component in self._components:
      if isinstance(component, component_class):
        return component

    return None

  def start(self):
    for component in self._components:
      component.start()

  def update(self):
    for component in self._components:
      component.update()

  def fixed_update(self) -> None:
    for component in self._components:
      component.fixed_update()

  def draw(self, screen: pygame.Surface) -> None:
    for component in self._components:
      component.draw(screen)
