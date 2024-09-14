import pygame
from src.core.game import Game
from src.core.scene import Scene
from src.core.game_object import GameObject
from typing import List
from src.interfaces.observer_interface import ObserverInterface

class BombermanGame(Game):
  def __init__(
      self,
      scene: Scene,
      observers: List[ObserverInterface] = [],
  ) -> None:
    super().__init__(scene, observers)
