from src.core.base_enum import BaseEnum
from os.path import join

class PowerEnum(BaseEnum):
  LIFE = 'Life'
  SKULL = 'Skull'

  def base_dir(self) -> str:
    dirs = {
      PowerEnum.LIFE: 'life_power',
      PowerEnum.SKULL: 'skull_power',
    }

    return join('assets', 'powers', dirs[self])
