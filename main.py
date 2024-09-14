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
from config import *

if __name__ == '__main__':
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

  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  display = ScoreDisplay(
    screen,
    GAME_DURATION,
    PLAYER_MAX_LIVES,
    player1_sprites,
    player2_sprites,
    PLAYER_1_NAME,
    PLAYER_2_NAME,
  )
  scene = MainScene(screen, display)

  observers = [display]

  game = BombermanGame(
    scene,
    GAME_DURATION,
    observers = observers,
  )
  game.run()
