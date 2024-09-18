
from src.core.base_object import BaseObject
from typing import List, Type, Dict, Callable, Tuple, MutableSet, Optional
from src.core.game_object import GameObject
import random
import time
import pygame
from config import DISPLAY_HEIGHT, BLOCK_SIZE
from src.enums.game_object_type_enum import GameObjectTypeEnum

class GameObjectManager(BaseObject):
  def __init__(self, tiles_width: int, tiles_height: int):
    self._game_objects: List[GameObject] = []

    self._tiles_width = tiles_width
    self._tiles_height = tiles_height
    self._tiles: List[List[GameObject]] = [[None for j in range(self._tiles_width)] for i in range(self._tiles_height)]

    self._main_game_objects: List[GameObject] = []

    self._time_to_sort_game_objects: float = 0.5
    self._time_last_sort: float = time.time()

  def add_game_object(self, game_object: GameObject) -> None:
    types = {
      GameObjectTypeEnum.NORMAL: lambda: self.__add(game_object),
      GameObjectTypeEnum.MAIN: lambda: self.__add_main(game_object),
      GameObjectTypeEnum.TILE: lambda: self.__add_tile(game_object),
    }

    types[game_object._type]()

  def __add_tile(self, game_object: GameObject) -> None:
    i: int = int((game_object._y - game_object._min_y) / BLOCK_SIZE)
    j: int = int((game_object._x - game_object._min_x) / BLOCK_SIZE)

    if self._tiles[i][j] is not None:
      self.remove_game_object(self._tiles[i][j])

    self._tiles[i][j] = game_object
    self.__add(game_object)

  def __add_main(self, game_object: GameObject) -> None:
    self._main_game_objects.append(game_object)
    self.__add(game_object)

  def __add(self, game_object: GameObject) -> None:
    self._game_objects.append(game_object)
    self.__sort_game_objects_by_order_in_layer()

  def remove_game_object(self, game_object: GameObject) -> None:
    types = {
      GameObjectTypeEnum.NORMAL: lambda: self.__remove(game_object),
      GameObjectTypeEnum.MAIN: lambda: self.__remove_main(game_object),
      GameObjectTypeEnum.TILE: lambda: self.__remove_tile(game_object),
    }

    types[game_object._type]()

  def __remove_tile(self, game_object: GameObject) -> None:
    stop: bool = False

    for i in range(self._tiles_height):
      for j in range(self._tiles_width):
        if self._tiles[i][j] == game_object:
          self._tiles[i][j] = None
          stop = True
          break

      if stop:
        break

    self.__remove(game_object)

  def __remove_main(self, game_object: GameObject) -> None:
    if game_object in self._main_game_objects:
      self._main_game_objects.remove(game_object)

    self.__remove(game_object)

  def __remove(self, game_object: GameObject):
    if game_object in self._game_objects:
      self._game_objects.remove(game_object)

  def get(self, game_object_class: Type[GameObject]):
    for game_object in self._game_objects:
      if isinstance(game_object, game_object_class):
          return game_object

    return None

  def start(self) -> None:
    for game_object in self._game_objects:
      game_object.start()

  def update(self) -> None:
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

  def __handle_collisions(self) -> None:
    for i in range(len(self._main_game_objects)):
      for j in range(i + 1, len(self._main_game_objects)):
        main_i = self._main_game_objects[i]
        main_j = self._main_game_objects[j]

        for layer_i in main_i._layers:
          for layer_j in main_j._layers:
            if layer_i == layer_j and main_i.is_colliding(main_j):
              main_i.on_collide(main_j, layer_i)
              main_j.on_collide(main_i, layer_j)

    for main_game_object in self._main_game_objects:
      collision_tiles = self.__get_collision_tiles(main_game_object)

      for collision_tile in collision_tiles:
        for layer_i in main_game_object._layers:
          for layer_j in collision_tile._layers:
            if layer_i == layer_j and main_game_object.is_colliding(collision_tile):
              main_game_object.on_collide(collision_tile, layer_i)
              collision_tile.on_collide(main_game_object, layer_j)

  def switch_debug_mode(self) -> None:
    for game_object in self._game_objects:
      game_object.switch_debug_mode()

  def __sort_game_objects_by_order_in_layer(self) -> None:
    key_func: Callable[[GameObject], Tuple[int, int]] = lambda game_object: (game_object.get_order_in_layer(), random.random())
    self._game_objects.sort(key = key_func)

  def __get_collision_tiles(self, game_object: GameObject) -> List[GameObject]:
    x = game_object._x
    y = game_object._y
    l = BLOCK_SIZE
    h = BLOCK_SIZE

    positions: List[Tuple[float, float]] = [(x, y), (x + l, y), (x + l, y + h), (x, y + h)]

    tile_positions: MutableSet[Tuple[int, int]] = set()
    for x_, y_ in positions:
      i = int((y_ - game_object._min_y) / h)
      j = int((x_ - game_object._min_x) / l)

      if i == self._tiles_height or j == self._tiles_width:
        continue

      tile_positions.add((i, j))

    return [self._tiles[i][j] for i, j in tile_positions if self._tiles[i][j] is not None]

