from src.core.base_enum import BaseEnum
from os.path import join

class PowerEnum(BaseEnum):
  LIFE = 'Life'
  SKULL = 'Skull'
  DROP_BOMB_CDR = 'Drop Bomb Cdr'

  def base_dir(self) -> str:
    dirs = {
      PowerEnum.LIFE: 'life_power',
      PowerEnum.SKULL: 'skull_power',
      PowerEnum.DROP_BOMB_CDR: 'drop_bomb_cdr_power',
    }

    return join('assets', 'powers', dirs[self])
