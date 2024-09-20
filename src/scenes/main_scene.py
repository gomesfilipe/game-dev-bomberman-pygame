from typing import List, Optional
from src.core.scene import Scene
import pygame
from config import *
from src.game_objects.player_game_object import PlayerGameObject
from src.game_objects.block_game_object import BlockGameObject
from src.game_objects.broken_block_game_object import BrokenBlockGameObject
from src.commands.movement_commands import MovementCommands
from src.commands.skill_commands import SkillCommands
from src.displays.score_display import ScoreDisplay
from src.enums.game_object_type_enum import GameObjectTypeEnum
from src.enums.player_type_enum import PlayerTypeEnum
from src.core.game_object_manager import GameObjectManager
from src.enums.event_enum import EventEnum

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

    self._player1_type: Optional[PlayerTypeEnum] = None
    self._player2_type: Optional[PlayerTypeEnum] = None
    self._winner_player_type: Optional[PlayerTypeEnum] = None

  def start(self) -> None:
    if self._display is not None:
      self._display.start()

    self._player1 = self._create_player1()
    self._player2 = self._create_player2()
    blocks = self._create_blocks()
    broken_blocks = self._create_broken_blocks()

    for block in blocks:
      self._game_object_manager.add_game_object(block)

    for broken_block in broken_blocks:
      self._game_object_manager.add_game_object(broken_block)

    self._display.set_players(self._player1, self._player2)
    self._game_object_manager.add_game_object(self._player1)
    self._game_object_manager.add_game_object(self._player2)

    self._game_object_manager.start()

  def set_player_types(self, player1_type: PlayerTypeEnum, player2_type: PlayerTypeEnum) -> None:
    self._player1_type = player1_type
    self._player2_type = player2_type

  def set_winner_player_type(self, player_type: PlayerTypeEnum) -> None:
    self._winner_player_type = player_type

  def winner_player_type(self) -> Optional[PlayerTypeEnum]:
    return self._winner_player_type

  def _create_blocks(self) -> List[BlockGameObject]:
    blocks: List[BlockGameObject] = []

    for j in range(self._tiles_width):
      blocks.append(self._new_block(0, j))
      blocks.append(self._new_block(self._tiles_height - 1, j))


    for i in range(1, self._tiles_height):
      blocks.append(self._new_block(i, 0))
      blocks.append(self._new_block(i, self._tiles_width - 1))

    for i in range(2, self._tiles_height - 2, 2):
      for j in range(2, self._tiles_width - 2, 2):
        blocks.append(self._new_block(i, j))

    return blocks

  def _create_broken_blocks(self) -> List[BrokenBlockGameObject]:
    broken_blocks: List[BrokenBlockGameObject] = []

    for i in range(2, self._tiles_height - 2):
      for j in range(2, self._tiles_width - 2):
        if i % 2 == 0 and j % 2 == 0:
          continue

        broken_blocks.append(self._new_broken_block(i, j))

    return broken_blocks

  def _create_player1(self) -> PlayerGameObject:
    return PlayerGameObject(
      self._player1_type.sprites(PLAYER_WIDTH, PLAYER_HEIGHT),
      PLAYER_VELOCITY,
      MovementCommands(pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT),
      SkillCommands(pygame.K_p),
      self._player1_type,
      PLAYER_MAX_LIVES,
      BLOCK_SIZE,
      DISPLAY_HEIGHT + BLOCK_SIZE,
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
      self._player2_type.sprites(PLAYER_WIDTH, PLAYER_HEIGHT),
      PLAYER_VELOCITY,
      MovementCommands(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d),
      SkillCommands(pygame.K_q),
      self._player2_type,
      PLAYER_MAX_LIVES,
      SCREEN_WIDTH - 2 * BLOCK_SIZE,
      SCREEN_HEIGHT - 2 * BLOCK_SIZE,
      PLAYER_GAME_OBJECT_ORDER_IN_LAYER,
      GameObjectTypeEnum.MAIN,
      PLAYER_2_NAME,
      layers = ['player2_collision', 'player2_power', 'player2_explosion'],
      min_x = 0.0,
      max_x = self.width(),
      min_y = self._display.height(),
      max_y = self.height(),
    )

  def _new_block(self, i: int, j: int) -> BlockGameObject:
    l = BLOCK_SPRITE.width()
    h = BLOCK_SPRITE.height()

    return BlockGameObject(
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

  def _new_broken_block(self, i: int, j: int) -> BrokenBlockGameObject:
    l = BLOCK_SPRITE.width()
    h = BLOCK_SPRITE.height()

    return BrokenBlockGameObject(
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

  def on_end_scene(self) -> None:
    player1_dead: bool = self._player1._status_manager.dead.is_active()
    player2_dead: bool = self._player2._status_manager.dead.is_active()
    
    if player1_dead and player2_dead:
      self._winner_player_type = None
    elif player1_dead:
      self._winner_player_type = self._player2.get_type()
    elif player2_dead:
      self._winner_player_type = self._player1.get_type()
    else:
      self._winner_player_type = None

    self._game_object_manager = GameObjectManager(self._tiles_width, self._tiles_height)

  def get_winner_player_type(self) -> PlayerTypeEnum:
    return self._winner_player_type
  
  def update(self) -> None:
    super().update()

    if self._player1._status_manager.dead.is_active() or self._player2._status_manager.dead.is_active():
      EventEnum.NEXT_SCENE.post_event()
