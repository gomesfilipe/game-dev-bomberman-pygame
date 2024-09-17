from src.core.game_object import GameObject
from src.game_objects.bomb_game_object import BombGameObject
from src.core.skill import Skill
from config import BOMB_CDR, BOMB_ORDER_IN_LAYER, EXPLOSION_TIME, EXPLOSION_RANGE, KICK_RANGE
from typing import Tuple
from src.enums.game_object_type_enum import GameObjectTypeEnum

class DropBombSkill(Skill):
  def __init__(self) -> None:
    super().__init__(BOMB_CDR)
    self._explosion_range = EXPLOSION_RANGE
    self._super_bomb: bool = False

  @Skill._execute_decorator
  def execute(self, game_object: GameObject) -> None:
    x_bomb, y_bomb = self.__bomb_position(game_object)

    width = game_object._sprites._hitbox.get_width()
    height = game_object._sprites._hitbox.get_height()

    game_object.instantiate(
      BombGameObject,
      x = x_bomb,
      y = y_bomb,
      size = (width, height),
      order_in_layer = BOMB_ORDER_IN_LAYER,
      game_object_type = GameObjectTypeEnum.NORMAL,
      explosion_time = EXPLOSION_TIME,
      explosion_range = self._explosion_range,
      kick_range = KICK_RANGE,
      super_bomb = self._super_bomb,
      layers = [],
      min_x = game_object._min_x,
      max_x = game_object._max_x,
      min_y = game_object._min_y,
      max_y = game_object._max_y,
    )

    self._super_bomb = False

  def __bomb_position(self, game_object: GameObject) -> Tuple[float, float]:
    width = game_object._sprites._hitbox.get_width()
    height = game_object._sprites._hitbox.get_height()
    min_x = game_object._min_x
    min_y = game_object._min_y

    x = round((game_object._x - min_x) / width) * width + min_x
    y = round((game_object._y - min_y) / height) * height + min_y

    return x, y

  def increase_explosion_range(self) -> None:
    self._explosion_range += 1

  def set_super_bomb(self) -> None:
    self._super_bomb = True
