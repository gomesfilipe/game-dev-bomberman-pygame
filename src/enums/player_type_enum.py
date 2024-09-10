from enum import Enum
from os.path import join

class PlayerTypeEnum(Enum):
  BEAR = 'Bear'
  CAT = 'Cat'
  DOG = 'Dog'
  MOUSE = 'Mouse'
  PIG = 'Pig'
  RABBIT = 'Rabbit'

  def assets_path(self) -> str:
    dirs = {
      PlayerTypeEnum.BEAR: 'BEAR',
      PlayerTypeEnum.CAT: 'CAT',
      PlayerTypeEnum.DOG: 'BEAR',
      PlayerTypeEnum.MOUSE: 'MOUSE',
      PlayerTypeEnum.PIG: 'PIG',
      PlayerTypeEnum.RABBIT: 'RABBIT',
    }

    return join('assets', 'animals', dirs[self], 'rotation preview')
