from src.core.base_object import BaseObject

class Component(BaseObject):
  pass

from src.core.game_object import GameObject

class Component(BaseObject):
  def __init__(self, game_object: GameObject, name = ''):
    super().__init__(name)
    self._game_object = game_object
