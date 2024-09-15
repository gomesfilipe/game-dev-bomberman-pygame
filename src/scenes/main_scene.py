from typing import List
from src.core.scene import Scene
import pygame
from config import *
from os.path import join
from src.sprites.player_sprites import PlayerSprites
from src.sprites.block_sprites import SimpleSprite
from src.game_objects.player_game_object import PlayerGameObject
from src.game_objects.block_game_object import BlockGameObject
from src.game_objects.broken_block_game_object import BrokenBlockGameObject
from src.utils.movement_commands import MovementCommands
from src.displays.score_display import ScoreDisplay

class MainScene(Scene):
  def __init__(
      self,
      screen: pygame.Surface,
      duration: int,
      background_color: str = 'white',
  ) -> None:
    display = ScoreDisplay(screen, duration)
    super().__init__(screen, display, background_color)
    self._display = display
    self._duration = duration

  def start(self) -> None:
    if self._display is not None:
      self._display.start()

    player1 = self._create_player1()
    player2 = self._create_player2()
    blocks = self._create_blocks()
    broken_blocks = self._create_broken_blocks()

    self._display.set_players(player1, player2)
    self._game_object_manager.add(player1)
    self._game_object_manager.add(player2)

    for block in blocks:
      self._game_object_manager.add(block)

    for broken_block in broken_blocks:
      self._game_object_manager.add(broken_block)

    self._game_object_manager.start()

  def _create_blocks(self) -> List[BlockGameObject]:
    block_sprites = SimpleSprite(join('assets', 'blocks', 'block_2.png'), (BLOCK_SIZE, BLOCK_SIZE))
    blocks: List[BlockGameObject] = []

    l = block_sprites.width()
    h = block_sprites.height()

    i: int = 1
    while (i + 1) * h + self._display.height() < self._screen.get_height():
      j: int = 1
      while (j + 1) * l < self._screen.get_width():
        blocks.append(
          BlockGameObject(
            block_sprites,
            j * h,
            i * l + self._display.height(),
            BLOCK_GAME_OBJECT_ORDER_IN_LAYER,
            layers = ['player1_collision', 'player2_collision'],
            min_x = 0.0,
            max_x = self._screen.get_width(),
            min_y = self._display.height(),
            max_y = self._screen.get_height(),
          )
        )

        j += 2
      i += 2

    return blocks

  def _create_broken_blocks(self) -> List[BrokenBlockGameObject]:
    broken_block_sprites = SimpleSprite(join('assets', 'blocks', 'hay_block.png'), (BLOCK_SIZE, BLOCK_SIZE))
    broken_blocks: List[BrokenBlockGameObject] = []

    l = broken_block_sprites.width()
    h = broken_block_sprites.height()

    i: int = 2
    while (i + 1) * h + self._display.height() < self._screen.get_height():
      j: int = 2
      while (j + 1) * l < self._screen.get_width():
        broken_blocks.append(
          BrokenBlockGameObject(
            broken_block_sprites,
            j * h,
            i * l + self._display.height(),
            BLOCK_GAME_OBJECT_ORDER_IN_LAYER,
            layers = ['player1_broken_block', 'player2_broken_block'],
            min_x = 0.0,
            max_x = self._screen.get_width(),
            min_y = self._display.height(),
            max_y = self._screen.get_height(),
          )
        )

        j += 2
      i += 2

    return broken_blocks

  def _create_player1(self) -> PlayerGameObject:
    player1_sprites = PlayerSprites(
      join(PLAYER_1_TYPE.rotation_assets_path(), '3 Back.png'),
      join(PLAYER_1_TYPE.rotation_assets_path(), '2 Left.png'),
      join(PLAYER_1_TYPE.rotation_assets_path(), '1 Front.png'),
      join(PLAYER_1_TYPE.rotation_assets_path(), '4 Right.png'),
      join(PLAYER_1_TYPE.face_assets_path(), 'face.png'),
      (PLAYER_WIDTH, PLAYER_HEIGHT),
    )

    return PlayerGameObject(
      player1_sprites,
      PLAYER_DELTA_TIME,
      PLAYER_VELOCITY,
      MovementCommands(pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT),
      PLAYER_1_TYPE,
      PLAYER_MAX_LIVES,
      0,
      DISPLAY_HEIGHT,
      PLAYER_GAME_OBJECT_ORDER_IN_LAYER,
      PLAYER_1_NAME,
      layers = ['player1_collision', 'player1_broken_block', 'player1_power'],
      min_x = 0.0,
      max_x = self._screen.get_width(),
      min_y = self._display.height(),
      max_y = self._screen.get_height(),
    )

  def _create_player2(self) -> PlayerGameObject:
    player2_sprites = PlayerSprites(
      join(PLAYER_2_TYPE.rotation_assets_path(), '3 Back.png'),
      join(PLAYER_2_TYPE.rotation_assets_path(), '2 Left.png'),
      join(PLAYER_2_TYPE.rotation_assets_path(), '1 Front.png'),
      join(PLAYER_2_TYPE.rotation_assets_path(), '4 Right.png'),
      join(PLAYER_2_TYPE.face_assets_path(), 'face.png'),
      (PLAYER_WIDTH, PLAYER_HEIGHT),
    )

    return PlayerGameObject(
      player2_sprites,
      PLAYER_DELTA_TIME,
      PLAYER_VELOCITY,
      MovementCommands(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d),
      PLAYER_2_TYPE,
      PLAYER_MAX_LIVES,
      SCREEN_WIDTH - PLAYER_WIDTH / 2,
      SCREEN_HEIGHT - PLAYER_HEIGHT / 2,
      PLAYER_GAME_OBJECT_ORDER_IN_LAYER,
      PLAYER_2_NAME,
      layers = ['player2_collision', 'player2_broken_block', 'player2_power'],
      min_x = 0.0,
      max_x = self._screen.get_width(),
      min_y = self._display.height(),
      max_y = self._screen.get_height(),
    )
