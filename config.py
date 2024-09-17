from src.enums.player_type_enum import PlayerTypeEnum
from src.enums.power_enum import PowerEnum
from src.sprites.player_sprites import PlayerSprites
from src.sprites.simple_sprite import SimpleSprite
from os.path import join
from typing import Tuple
import pygame

PLAYER_1_TYPE: PlayerTypeEnum = PlayerTypeEnum.MOUSE
PLAYER_2_TYPE: PlayerTypeEnum = PlayerTypeEnum.CAT

PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64

PLAYER_1_NAME = 'player1'
PLAYER_2_NAME = 'player2'

PLAYER_VELOCITY: float = 100
PLAYER_MAX_LIVES: int = 5

PLAYER_GAME_OBJECT_ORDER_IN_LAYER: int = 2
POWER_GAME_OBJECT_ORDER_IN_LAYER: int = 1
BLOCK_GAME_OBJECT_ORDER_IN_LAYER: int = 1
BOMB_ORDER_IN_LAYER: int = 2
EXPLOSION_ORDER_IN_LAYER: int = 3

BLOCK_SIZE: int = 32
DISPLAY_HEIGHT: int = 80

GAME_DURATION: int = 300

SCREEN_WIDTH: int = BLOCK_SIZE * 15
SCREEN_HEIGHT: int = DISPLAY_HEIGHT + BLOCK_SIZE * 11

PROBABILITY_SPAWN_POWER: float = 1

EXPLOSION_TIME: int = 3
EXPLOSION_RANGE: int = 1
KICK_RANGE: int = 4
BOMB_CDR: float = 2

DROP_BOMB_CDR: float = 0.2
EXPLOSION_DURATION: float = 1.0

NONE_STATUS_DURATION: float = float('inf')
IMMUNE_STATUS_DURATION: float = 3.0
DEAD_STATUS_DURATION: float = float('inf')

POWER_SIZE: Tuple[int, int] = (BLOCK_SIZE / 2, BLOCK_SIZE / 2)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

PLAYER_1_SPRITES = PlayerSprites(
  join(PLAYER_1_TYPE.rotation_assets_path(), '3 Back.png'),
  join(PLAYER_1_TYPE.rotation_assets_path(), '2 Left.png'),
  join(PLAYER_1_TYPE.rotation_assets_path(), '1 Front.png'),
  join(PLAYER_1_TYPE.rotation_assets_path(), '4 Right.png'),
  join(PLAYER_1_TYPE.face_assets_path(), 'face.png'),
  join(PLAYER_1_TYPE.base_dir(), 'Left', 'death.png'),
  join(PLAYER_1_TYPE.base_dir(), 'Right', 'death.png'),
  (PLAYER_WIDTH, PLAYER_HEIGHT),
)

PLAYER_2_SPRITES = PlayerSprites(
  join(PLAYER_2_TYPE.rotation_assets_path(), '3 Back.png'),
  join(PLAYER_2_TYPE.rotation_assets_path(), '2 Left.png'),
  join(PLAYER_2_TYPE.rotation_assets_path(), '1 Front.png'),
  join(PLAYER_2_TYPE.rotation_assets_path(), '4 Right.png'),
  join(PLAYER_2_TYPE.face_assets_path(), 'face.png'),
  join(PLAYER_2_TYPE.base_dir(), 'Left', 'death.png'),
  join(PLAYER_2_TYPE.base_dir(), 'Right', 'death.png'),
  (PLAYER_WIDTH, PLAYER_HEIGHT),
)

EXPLOSION_SPRITE = SimpleSprite(join('assets', 'explosion', 'explosion.png'), (BLOCK_SIZE, BLOCK_SIZE))
BOMB_SPRITE = SimpleSprite(join('assets', 'bomb', 'bomb.png'), (BLOCK_SIZE, BLOCK_SIZE))
BLOCK_SPRITE = SimpleSprite(join('assets', 'blocks', 'block_2.png'), (BLOCK_SIZE, BLOCK_SIZE))
BROKEN_BLOCK_SPRITE = SimpleSprite(join('assets', 'blocks', 'hay_block.png'), (BLOCK_SIZE, BLOCK_SIZE))
DROP_BOMB_CDR_POWER_SPRITE = SimpleSprite(join(PowerEnum.DROP_BOMB_CDR.base_dir(), 'drop_bomb_cdr_power.png'), POWER_SIZE)
INCREASE_EXPLOSION_RANGE_POWER_SPRITE = SimpleSprite(join(PowerEnum.INCREASE_EXPLOSION_RANGE.base_dir(), 'increase_explosion_range_power.png'), POWER_SIZE)
LIFE_POWER_SPRITE = SimpleSprite(join(PowerEnum.LIFE.base_dir(), 'life_power.png'), POWER_SIZE)
SKULL_POWER_SPRITE = SimpleSprite(join(PowerEnum.SKULL.base_dir(), 'skull_power.png'), POWER_SIZE)
SUPER_BOMB_POWER_SPRITE = SimpleSprite(join(PowerEnum.SUPER_BOMB.base_dir(), 'super_bomb_power.png'), POWER_SIZE)
