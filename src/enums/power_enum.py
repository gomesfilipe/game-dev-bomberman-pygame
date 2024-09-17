from src.core.base_enum import BaseEnum
from os.path import join

class PowerEnum(BaseEnum):
  LIFE = 'Life'
  SKULL = 'Skull'
  DROP_BOMB_CDR = 'Drop Bomb Cdr'
  INCREASE_EXPLOSION_RANGE = 'Increase Explosion Range'
  SUPER_BOMB = 'Super Bomb'

  def base_dir(self) -> str:
    dirs = {
      PowerEnum.LIFE: 'life_power',
      PowerEnum.SKULL: 'skull_power',
      PowerEnum.DROP_BOMB_CDR: 'drop_bomb_cdr_power',
      PowerEnum.INCREASE_EXPLOSION_RANGE: 'increase_explosion_range_power',
      PowerEnum.SUPER_BOMB: 'super_bomb_power',
    }

    return join('assets', 'powers', dirs[self])
