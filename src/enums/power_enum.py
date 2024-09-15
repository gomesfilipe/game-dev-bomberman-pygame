from src.core.base_enum import BaseEnum
from typing import Type
from src.game_objects.power_game_object import PowerGameObject
from src.game_objects.life_power_game_object import LifePowerGameObject
from src.game_objects.skull_power_game_object import SkullPowerGameObject
import random

class PowerEnum(BaseEnum):
  LIFE = 'Life'
  SKULL = 'Skull'

  def power_class(self) -> Type[PowerGameObject]:
    power_classes = {
      PowerEnum.LIFE: LifePowerGameObject,
      PowerEnum.SKULL: SkullPowerGameObject,
    }

    return power_classes[self]

  @classmethod
  def random_power_class(cls) -> Type[PowerGameObject]:
    power: PowerEnum = random.choice(cls.cases())
    return power.power_class()
