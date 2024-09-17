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

class MainScene(Scene):
  def __init__(
    self,
    width: float,
    height: float,
    duration: int,
    background_color: str = 'white',
  ) -> None:
    display = ScoreDisplay(width, DISPLAY_HEIGHT, duration)
    super().__init__(width, height, display, background_color)
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
    blocks: List[BlockGameObject] = []

    l = BLOCK_SPRITE.width()
    h = BLOCK_SPRITE.height()

    i: int = 1
    while (i + 1) * h + self._display.height() < self.height():
      j: int = 1
      while (j + 1) * l < self.width():
        blocks.append(
          BlockGameObject(
            BLOCK_SPRITE,
            j * h,
            i * l + self._display.height(),
            BLOCK_GAME_OBJECT_ORDER_IN_LAYER,
            layers = ['player1_collision', 'player2_collision', 'explosion'],
            min_x = 0.0,
            max_x = self.width(),
            min_y = self._display.height(),
            max_y = self.height(),
          )
        )

        j += 2
      i += 2

    return blocks

  def _create_broken_blocks(self) -> List[BrokenBlockGameObject]:
    broken_blocks: List[BrokenBlockGameObject] = []

    l = BROKEN_BLOCK_SPRITE.width()
    h = BROKEN_BLOCK_SPRITE.height()

    i: int = 2
    while (i + 1) * h + self._display.height() < self.height():
      # if i % 2 == 0:
      #   j = 1
      # else:
      j = 2

      while (j + 1) * l < self.width():
        broken_blocks.append(
          BrokenBlockGameObject(
            BROKEN_BLOCK_SPRITE,
            j * h,
            i * l + self._display.height(),
            BLOCK_GAME_OBJECT_ORDER_IN_LAYER,
            layers = ['explosion', 'player1_collision', 'player2_collision'],
            min_x = 0.0,
            max_x = self.width(),
            min_y = self._display.height(),
            max_y = self.height(),
          )
        )
        # if i % 2 == 0:
        #   j += 1
        # else:
        j += 2
      i += 2

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
      PLAYER_2_NAME,
      layers = ['player2_collision', 'player2_power', 'player2_explosion'],
      min_x = 0.0,
      max_x = self.width(),
      min_y = self._display.height(),
      max_y = self.height(),
    )
