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
from src.enums.player_type_enum import PlayerTypeEnum

class ChoosePlayersScene(Scene):
  def __init__(
    self,
    width: float,
    height: float,
    tiles_width: int,
    tiles_height: int,
    background_color: str = 'white',
  ) -> None:
    super().__init__(width, height, tiles_width, tiles_height, None, background_color)
    player_types: List[PlayerTypeEnum] = PlayerTypeEnum.cases()

    self._sprites = [player_type.single_sprite(256, 256) for player_type in player_types]

    self._player1_options = player_types.copy()
    self._player2_options = player_types.copy()

    self._player1_selected_index = 0
    self._player2_selected_index = 0

  def _current_player1_sprite(self) -> SimpleSprite:
    return self._sprites[self._player1_selected_index]

  def _current_player2_sprite(self) -> SimpleSprite:
    return self._sprites[self._player2_selected_index]

  def _next_player1_index(self) -> int:
    return (self._player1_selected_index + 1) % len(self._player1_options)

  def _next_player2_index(self) -> int:
    return (self._player2_selected_index + 1) % len(self._player2_options)

  def start(self) -> None:
    self._font: pygame.font.Font = pygame.font.SysFont('impact', 48)

  def draw(self, screen: pygame.Surface) -> None:
    screen.fill(self._background_color)

    if self._display is not None:
      self._display.draw(screen)

    self.__draw_title(screen)
    self.__draw_selected_player1(screen)
    self.__draw_selected_player2(screen)
    self.__draw_start_button(screen)

    pygame.display.flip()

  def __draw_title(self, screen: pygame.Surface) -> None:
    pygame.draw.rect(screen, 'black', (0, 0, screen.get_width(), 80))

    title: str = 'Bomberman: Animal Revolution'
    title_image = self._font.render(f'{title}', True, (255, 255, 255))
    x = (self.width() - title_image.get_width()) / 2
    y = (80 - title_image.get_height()) / 2
    screen.blit(title_image, (x, y))

  def __draw_selected_player1(self, screen: pygame.Surface) -> None:
    sprite = self._current_player1_sprite()
    screen.blit(sprite.idle(), (10, (screen.get_height() - 160 - sprite.height()) / 2 + 80))

  def __draw_selected_player2(self, screen: pygame.Surface) -> None:
    sprite = self._current_player2_sprite()
    screen.blit(sprite.idle(), (screen.get_width() - 30 - sprite.width(), (screen.get_height() - 160 - sprite.height()) / 2 + 80))

  def __draw_start_button(self, screen: pygame.Surface) -> None:
    pygame.draw.rect(screen, 'black', (0, screen.get_height() - 80, screen.get_width(), 80))

    label: str = 'Start Game'
    label_image = self._font.render(f'{label}', True, (255, 255, 255))
    x = (self.width() - label_image.get_width()) / 2
    y = (screen.get_height() - (80 - label_image.get_height()) / 2) - label_image.get_height()
    screen.blit(label_image, (x, y))
