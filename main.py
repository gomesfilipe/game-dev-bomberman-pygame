from src.games.bomberman_game import BombermanGame
from src.scenes.main_scene import MainScene
from src.game_objects.player_game_object import PlayerGameObject
from src.displays.score_display import ScoreDisplay
from src.enums.player_type_enum import PlayerTypeEnum
from src.utils.player_commands import PlayerCommands
from src.sprites.player_sprites import PlayerSprites
from os.path import join
from typing import Tuple
import pygame

if __name__ == '__main__':
  PLAYER_1_TYPE: PlayerTypeEnum = PlayerTypeEnum.CAT
  PLAYER_2_TYPE: PlayerTypeEnum = PlayerTypeEnum.MOUSE
  SPRITES_SIZE: Tuple[int, int] = (64, 64)
  DELTA_TIME: int = 1
  VELOCITY: float = 0.1
  MAX_LIVES: int = 5
  GAME_DURATION: int = 300


  player1_sprites = PlayerSprites(
    join(PLAYER_1_TYPE.rotation_assets_path(), '3 Back.png'),
    join(PLAYER_1_TYPE.rotation_assets_path(), '2 Left.png'),
    join(PLAYER_1_TYPE.rotation_assets_path(), '1 Front.png'),
    join(PLAYER_1_TYPE.rotation_assets_path(), '4 Right.png'),
    join(PLAYER_1_TYPE.face_assets_path(), 'face.png'),
    SPRITES_SIZE,
  )

  player2_sprites = PlayerSprites(
    join(PLAYER_2_TYPE.rotation_assets_path(), '3 Back.png'),
    join(PLAYER_2_TYPE.rotation_assets_path(), '2 Left.png'),
    join(PLAYER_2_TYPE.rotation_assets_path(), '1 Front.png'),
    join(PLAYER_2_TYPE.rotation_assets_path(), '4 Right.png'),
    join(PLAYER_2_TYPE.face_assets_path(), 'face.png'),
    SPRITES_SIZE,
  )

  screen = pygame.display.set_mode((640, 480))
  display = ScoreDisplay(screen, GAME_DURATION, MAX_LIVES, player1_sprites, player2_sprites)
  scene = MainScene(screen, display)


  player1 = PlayerGameObject(
    player1_sprites,
    scene,
    DELTA_TIME,
    VELOCITY,
    PlayerCommands(pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT),
    PLAYER_1_TYPE,
    MAX_LIVES,
    layers = []
  )

  player2 = PlayerGameObject(
    player2_sprites,
    scene,
    DELTA_TIME,
    VELOCITY,
    PlayerCommands(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d),
    PLAYER_2_TYPE,
    MAX_LIVES,
    layers = []
  )


  game_objects = [player1, player2]
  # observers = [display]

  game = BombermanGame(
    scene,
    game_objects,
    GAME_DURATION,
    # observers = observers,
  )
  game.run()
