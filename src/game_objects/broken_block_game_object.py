from typing import List
from src.game_objects.game_object import GameObject
from src.game_objects.block_game_object import BlockGameObject
from src.sprites.block_sprites import BlockSprites
from src.scenes.scene import Scene
from typing import Dict, Callable
import pygame

class BrokenBlockGameObject(BlockGameObject):
  def __init__(
      self,
      sprites: BlockSprites,
      scene: Scene,
      x: float,
      y: float,
      order_in_layer: int,
      layers: List[str] = [],
    ) -> None:
    super().__init__(sprites, scene, x, y, order_in_layer, layers)

  def on_collide(self, other: GameObject, layer: str) -> None:
    handlers: Dict[str, Callable] = {
      'player1_broken_block': lambda: self.__handle_player_broken_block_layer(other),
      'player2_broken_block': lambda: self.__handle_player_broken_block_layer(other),
    }

    if layer in handlers:
      handlers[layer]()

  def __handle_player_broken_block_layer(self, other: GameObject) -> None:
    self.destroy()
