from typing import List
from src.core.scene import Scene
import pygame
from config import *
from os.path import join
from src.sprites.player_sprites import PlayerSprites
from src.sprites.simple_sprite import SimpleSprite
from src.game_objects.player_game_object import PlayerGameObject
from src.game_objects.block_game_object import BlockGameObject
from src.game_objects.broken_block_game_object import BrokenBlockGameObject
from src.commands.movement_commands import MovementCommands
from src.commands.skill_commands import SkillCommands
from src.displays.score_display import ScoreDisplay
from src.enums.game_object_type_enum import GameObjectTypeEnum

class MainScene(Scene):
  def __init__(
    self,
    width: float,
    height: float,
    tiles_width: int,
    tiles_height: int,
    duration: int,
    background_color: str = 'white',
  ) -> None:
    display = ScoreDisplay(width, DISPLAY_HEIGHT, duration)
    super().__init__(width, height, tiles_width, tiles_height, display, background_color)
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
    self._game_object_manager.add_game_object(player1)
    self._game_object_manager.add_game_object(player2)

    for block in blocks:
      self._game_object_manager.add_game_object(block)

    for broken_block in broken_blocks:
      self._game_object_manager.add_game_object(broken_block)

    self._game_object_manager.start()

  def _create_blocks(self) -> List[BlockGameObject]:
    blocks: List[BlockGameObject] = []

    l = BLOCK_SPRITE.width()
    h = BLOCK_SPRITE.height()

    i: int = 1
    while (i + 1) * h + self._display.height() < self.height():
      j: int = 1
      while (j + 1) * l < self.width():
        block = BlockGameObject(
          BLOCK_SPRITE,
          j * h,
          i * l + self._display.height(),
          BLOCK_GAME_OBJECT_ORDER_IN_LAYER,
          GameObjectTypeEnum.TILE,
          layers = ['player1_collision', 'player2_collision', 'explosion'],
          min_x = 0.0,
          max_x = self.width(),
          min_y = self._display.height(),
          max_y = self.height(),
        )

        self._game_object_manager.add_game_object(blocks, i, j)   
        blocks.append(block)

        j += 2
      i += 2

    return blocks

  def _create_broken_blocks(self) -> List[BrokenBlockGameObject]:
    broken_blocks: List[BrokenBlockGameObject] = []

    l = BROKEN_BLOCK_SPRITE.width()
    h = BROKEN_BLOCK_SPRITE.height()

    i: int = 1
    while (i + 1) * h + self._display.height() < self.height():
      if i % 2 == 0:
        j = 1
      else:
        j = 2

      while (j + 1) * l < self.width():
        broken_block = BrokenBlockGameObject(
          BROKEN_BLOCK_SPRITE,
          j * h,
          i * l + self._display.height(),
          BLOCK_GAME_OBJECT_ORDER_IN_LAYER,
          GameObjectTypeEnum.TILE,
          layers = ['explosion', 'player1_collision', 'player2_collision'],
          min_x = 0.0,
          max_x = self.width(),
          min_y = self._display.height(),
          max_y = self.height(),
        )

        self._game_object_manager.add_game_object(broken_block, i, j)        
        broken_blocks.append(broken_block)

        if i % 2 == 0:
          j += 1
        else:
          j += 2
      i += 1

    return broken_blocks

  def _create_player1(self) -> PlayerGameObject:
    return PlayerGameObject(
      PLAYER_1_SPRITES,
      PLAYER_VELOCITY,
      MovementCommands(pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT),
      SkillCommands(pygame.K_p),
      PLAYER_1_TYPE,
      PLAYER_MAX_LIVES,
      0,
      DISPLAY_HEIGHT,
      PLAYER_GAME_OBJECT_ORDER_IN_LAYER,
      GameObjectTypeEnum.MAIN,
      PLAYER_1_NAME,
      layers = ['player1_collision', 'player1_power', 'player1_explosion'],
      min_x = 0.0,
      max_x = self.width(),
      min_y = self._display.height(),
      max_y = self.height(),
    )

  def _create_player2(self) -> PlayerGameObject:
    return PlayerGameObject(
      PLAYER_2_SPRITES,
      PLAYER_VELOCITY,
      MovementCommands(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d),
      SkillCommands(pygame.K_q),
      PLAYER_2_TYPE,
      PLAYER_MAX_LIVES,
      SCREEN_WIDTH - PLAYER_WIDTH / 2,
      SCREEN_HEIGHT - PLAYER_HEIGHT / 2,
      PLAYER_GAME_OBJECT_ORDER_IN_LAYER,
      GameObjectTypeEnum.MAIN,
      PLAYER_2_NAME,
      layers = ['player2_collision', 'player2_power', 'player2_explosion'],
      min_x = 0.0,
      max_x = self.width(),
      min_y = self._display.height(),
      max_y = self.height(),
    )
