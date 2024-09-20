from src.core.base_enum import BaseEnum
from src.sprites.simple_sprite import SimpleSprite
from src.sprites.player_sprites import PlayerSprites
from os.path import join

class PlayerTypeEnum(BaseEnum):
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

  def single_sprite(self, width: int, height: int) -> SimpleSprite:
    return SimpleSprite(
      join(self.rotation_assets_path(), '1 Front.png'),
      (width, height),
    )

  def sprites(self, width: int, height: int) -> SimpleSprite:
    return PlayerSprites(
      join(self.rotation_assets_path(), '3 Back.png'),
      join(self.rotation_assets_path(), '2 Left.png'),
      join(self.rotation_assets_path(), '1 Front.png'),
      join(self.rotation_assets_path(), '4 Right.png'),
      join(self.face_assets_path(), 'face.png'),
      join(self.base_dir(), 'Left', 'death.png'),
      join(self.base_dir(), 'Right', 'death.png'),
      (width, height),
    )
