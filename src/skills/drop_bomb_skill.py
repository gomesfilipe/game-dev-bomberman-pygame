from src.core.game_object import GameObject
from src.game_objects.bomb_game_object import BombGameObject
from src.core.skill import Skill
from config import BOMB_CDR, BOMB_ORDER_IN_LAYER, EXPLOSION_TIME, EXPLOSION_RANGE, KICK_RANGE
from typing import Tuple

class DropBombSkill(Skill):
  def __init__(self) -> None:
    super().__init__(BOMB_CDR)

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
      explosion_time = EXPLOSION_TIME,
      explosion_range = EXPLOSION_RANGE,
      kick_range = KICK_RANGE,
      layers = [],
      min_x = game_object._min_x,
      max_x = game_object._max_x,
      min_y = game_object._min_y,
      max_y = game_object._max_y,
    )

  def __bomb_position(self, game_object: GameObject) -> Tuple[float, float]:
    width = game_object._sprites._hitbox.get_width()
    height = game_object._sprites._hitbox.get_height()
    min_x = game_object._min_x
    min_y = game_object._min_y

    x = round((game_object._x - min_x) / width) * width + min_x
    y = round((game_object._y - min_y) / height) * height + min_y

    return x, y
