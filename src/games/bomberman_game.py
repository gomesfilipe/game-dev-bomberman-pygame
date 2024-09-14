import pygame
from src.games.game import Game
from src.scenes.scene import Scene
from src.game_objects.game_object import GameObject
from typing import List
from src.interfaces.observer_interface import ObserverInterface

class BombermanGame(Game):
  def __init__(
      self,
      scene: Scene,
      duration: int,
      observers: List[ObserverInterface] = [],
  ) -> None:
    super().__init__(scene, observers)

    self._duration = duration
