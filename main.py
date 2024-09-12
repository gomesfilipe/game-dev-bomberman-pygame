from src.games.bomberman_game import BombermanGame
from src.scenes.main_scene import MainScene
from src.game_objects.player_game_object import PlayerGameObject
from src.game_objects.block_game_object import BlockGameObject
from src.game_objects.broken_block_game_object import BrokenBlockGameObject
from src.displays.score_display import ScoreDisplay
from src.enums.player_type_enum import PlayerTypeEnum
from src.utils.player_commands import PlayerCommands
from src.sprites.player_sprites import PlayerSprites
from src.sprites.block_sprites import SimpleSprite
from os.path import join
from typing import Tuple, List
import pygame

def create_blocks() -> List[BlockGameObject]:
  blocks: List[BlockGameObject] = []

  l = block_sprites.width()
  h = block_sprites.height()

  i: int = 1
  while (i + 1) * h + display.height() < scene.get_screen().get_height():
    j: int = 1
    while (j + 1) * l < scene.get_screen().get_width():
      blocks.append(
        BlockGameObject(
          block_sprites,
          scene,
          j * h,
          i * l + display.height(),
          BLOCK_GAME_OBJECT_ORDER_IN_LAYER,
          layers = ['player1_collision', 'player2_collision'],
        )
      )

      j += 2
    i += 2

  return blocks

def create_broken_blocks() -> List[BrokenBlockGameObject]:
  broken_blocks: List[BrokenBlockGameObject] = []

  l = broken_block_sprites.width()
  h = broken_block_sprites.height()

  i: int = 2
  while (i + 1) * h + display.height() < scene.get_screen().get_height():
    j: int = 2
    while (j + 1) * l < scene.get_screen().get_width():
      broken_blocks.append(
        BrokenBlockGameObject(
          broken_block_sprites,
          scene,
          j * h,
          i * l + display.height(),
          BLOCK_GAME_OBJECT_ORDER_IN_LAYER,
          layers = ['player1_broken_block', 'player2_broken_block'],
        )
      )

      j += 2
    i += 2

  return broken_blocks

if __name__ == '__main__':
  PLAYER_1_TYPE: PlayerTypeEnum = PlayerTypeEnum.PIG
  PLAYER_2_TYPE: PlayerTypeEnum = PlayerTypeEnum.RABBIT

  PLAYER_WIDTH = 64
  PLAYER_HEIGHT = 64

  PLAYER_VELOCITY: float = 0.2
  PLAYER_MAX_LIVES: int = 5
  PLAYER_DELTA_TIME: int = 1

  PLAYER_GAME_OBJECT_ORDER_IN_LAYER = 1
  BLOCK_GAME_OBJECT_ORDER_IN_LAYER = 0

  BLOCK_SIZE: int = 32
  DISPLAY_HEIGHT: int = 80

  GAME_DURATION: int = 300

  SCREEN_WIDTH: int = BLOCK_SIZE * 15
  SCREEN_HEIGHT: int = DISPLAY_HEIGHT + BLOCK_SIZE * 11

  player1_sprites = PlayerSprites(
    join(PLAYER_1_TYPE.rotation_assets_path(), '3 Back.png'),
    join(PLAYER_1_TYPE.rotation_assets_path(), '2 Left.png'),
    join(PLAYER_1_TYPE.rotation_assets_path(), '1 Front.png'),
    join(PLAYER_1_TYPE.rotation_assets_path(), '4 Right.png'),
    join(PLAYER_1_TYPE.face_assets_path(), 'face.png'),
    (PLAYER_WIDTH, PLAYER_HEIGHT),
  )

  player2_sprites = PlayerSprites(
    join(PLAYER_2_TYPE.rotation_assets_path(), '3 Back.png'),
    join(PLAYER_2_TYPE.rotation_assets_path(), '2 Left.png'),
    join(PLAYER_2_TYPE.rotation_assets_path(), '1 Front.png'),
    join(PLAYER_2_TYPE.rotation_assets_path(), '4 Right.png'),
    join(PLAYER_2_TYPE.face_assets_path(), 'face.png'),
    (PLAYER_WIDTH, PLAYER_HEIGHT),
  )

  block_sprites = SimpleSprite(join('assets', 'blocks', 'block_2.png'), (BLOCK_SIZE, BLOCK_SIZE))
  broken_block_sprites = SimpleSprite(join('assets', 'blocks', 'hay_block.png'), (BLOCK_SIZE, BLOCK_SIZE))

  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  display = ScoreDisplay(screen, GAME_DURATION, PLAYER_MAX_LIVES, player1_sprites, player2_sprites)
  scene = MainScene(screen, display)

  player1 = PlayerGameObject(
    player1_sprites,
    scene,
    PLAYER_DELTA_TIME,
    PLAYER_VELOCITY,
    PlayerCommands(pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT),
    PLAYER_1_TYPE,
    PLAYER_MAX_LIVES,
    0,
    DISPLAY_HEIGHT,
    PLAYER_GAME_OBJECT_ORDER_IN_LAYER,
    layers = ['player1_collision', 'player1_broken_block'],
  )

  player2 = PlayerGameObject(
    player2_sprites,
    scene,
    PLAYER_DELTA_TIME,
    PLAYER_VELOCITY,
    PlayerCommands(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d),
    PLAYER_2_TYPE,
    PLAYER_MAX_LIVES,
    SCREEN_WIDTH - PLAYER_WIDTH / 2,
    SCREEN_HEIGHT - PLAYER_HEIGHT / 2,
    PLAYER_GAME_OBJECT_ORDER_IN_LAYER,
    layers = ['player2_collision', 'player2_broken_block'],
  )

  blocks = create_blocks()

  broken_blocks = create_broken_blocks()

  game_objects = [player1, player2] + blocks + broken_blocks

  # observers = [display]

  game = BombermanGame(
    scene,
    game_objects,
    GAME_DURATION,
    # observers = observers,
  )
  game.run()
