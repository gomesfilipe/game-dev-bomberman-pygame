from enum import Enum
from os.path import join

class PlayerTypeEnum(Enum):
  BEAR = 'Bear'
  CAT = 'Cat'
  DOG = 'Dog'
  MOUSE = 'Mouse'
  PIG = 'Pig'
  RABBIT = 'Rabbit'

  def base_dir(self) -> str:
    dirs = {
      PlayerTypeEnum.BEAR: 'BEAR',
      PlayerTypeEnum.CAT: 'CAT',
      PlayerTypeEnum.DOG: 'DOG',
      PlayerTypeEnum.MOUSE: 'MOUSE',
      PlayerTypeEnum.PIG: 'PIG',
      PlayerTypeEnum.RABBIT: 'RABBIT',
    }

    return join('assets', 'animals', dirs[self])

  def rotation_assets_path(self) -> str:
    return join(self.base_dir(), 'rotation preview')

  def face_assets_path(self) -> str:
    return join(self.base_dir(), 'face')
