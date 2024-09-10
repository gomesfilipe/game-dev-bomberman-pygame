from src.games.kill_fly_game import KillFlyGame
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
  PLAYER_1_TYPE: PlayerTypeEnum = PlayerTypeEnum.RABBIT
  PLAYER_2_TYPE: PlayerTypeEnum = PlayerTypeEnum.PIG
  SPRITES_SIZE: Tuple[int, int] = (64, 64)
  DELTA_TIME: int = 1
  VELOCITY: float = 0.1

  screen = pygame.display.set_mode((640, 480))

  display = ScoreDisplay(screen)
  scene = MainScene(screen, display)

  player1 = PlayerGameObject(
    PlayerSprites(
      join(PLAYER_1_TYPE.assets_path(), '3 Back.png'),
      join(PLAYER_1_TYPE.assets_path(), '2 Left.png'),
      join(PLAYER_1_TYPE.assets_path(), '1 Front.png'),
      join(PLAYER_1_TYPE.assets_path(), '4 Right.png'),
      SPRITES_SIZE,
    ),
    scene,
    DELTA_TIME,
    VELOCITY,
    PlayerCommands(pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT),
    layers = []
  )

  player2 = PlayerGameObject(
    PlayerSprites(
      join(PLAYER_2_TYPE.assets_path(), '3 Back.png'),
      join(PLAYER_2_TYPE.assets_path(), '2 Left.png'),
      join(PLAYER_2_TYPE.assets_path(), '1 Front.png'),
      join(PLAYER_2_TYPE.assets_path(), '4 Right.png'),
      SPRITES_SIZE,
    ),
    scene,
    DELTA_TIME,
    VELOCITY,
    PlayerCommands(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d),
    layers = []
  )

  game_objects = [player1, player2]
  # observers = [display]

  game = KillFlyGame(
    scene,
    game_objects,
    # observers = observers,
  )
  game.run()
