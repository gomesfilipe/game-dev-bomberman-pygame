from src.core.display import Display
from typing import Optional
import pygame
import time
from src.utils.utils import format_seconds_to_min_sec
from src.game_objects.player_game_object import PlayerGameObject
from src.components.skill_controller_component import SkillControllerComponent
from src.enums.event_enum import EventEnum

class ScoreDisplay(Display):
  def __init__(
    self,
    width: float,
    height: float,
    duration: int,
  ) -> None:
    super().__init__(width, height)

    self._duration = duration
    self._player1: Optional[PlayerGameObject] = None
    self._player2: Optional[PlayerGameObject] = None

  def start(self) -> None:
    self._start_time: int = int(time.time())
    self._time_spent: int = 0
    self._font: pygame.font.Font = pygame.font.SysFont('impact', 48)
    self._cdr_font: pygame.font.Font = pygame.font.SysFont('impact', 32)
    self._remaining_time: int = self._duration

  def update(self) -> None:
    self._time_spent = int(time.time() - self._start_time)
    self._remaining_time = max(self._duration - self._time_spent, 0)

    if self._remaining_time == 0:
      EventEnum.END_OF_GAME.post_event()

  def set_players(self, player1: PlayerGameObject, player2: PlayerGameObject) -> None:
    self._player1 = player1
    self._player2 = player2

  def draw(self, screen: pygame.Surface) -> None:
    self.__draw_background_rect(screen)
    self.__draw_player1_image(screen)
    self.__draw_player2_image(screen)
    self.__draw_player1_bomb_cdr(screen)
    self.__draw_player2_bomb_cdr(screen)
    self.__draw_remainig_time(screen)
    self.__draw_player1_lives(screen)
    self.__draw_player2_lives(screen)

  def __draw_background_rect(self, screen: pygame.Surface) -> None:
    pygame.draw.rect(screen, 'black', (0, 0, self.width(), self.height()))

  def __draw_player1_image(self, screen: pygame.Surface) -> None:
    player1_image = self._player1._sprites.face()
    x = (self.height() - player1_image.get_height()) / 2
    screen.blit(player1_image, (x, x))

  def __draw_player2_image(self, screen: pygame.Surface) -> None:
    player2_image = self._player2._sprites.face()
    y = (self.height() - player2_image.get_height()) / 2
    x = self.width() - y - player2_image.get_width()
    screen.blit(player2_image, (x, y))

  def __draw_player1_bomb_cdr(self, screen: pygame.Surface) -> None:
    skill_component: Optional[SkillControllerComponent] = self._player1.get_component(SkillControllerComponent)

    if skill_component is None:
      return

    drop_bomb_skill = skill_component._dromp_bomb_skill
    remaining_cdr: float = max(0.0, drop_bomb_skill._cdr - time.time() + drop_bomb_skill._last_use)

    remaining_cdr_image = self._cdr_font.render(f'{remaining_cdr:.2f}', True, (255, 255, 255))
    x = self.height() + remaining_cdr_image.get_width()
    y = (self.height() - remaining_cdr_image.get_height()) / 2
    screen.blit(remaining_cdr_image, (x, y))

  def __draw_player2_bomb_cdr(self, screen: pygame.Surface) -> None:
    skill_component: Optional[SkillControllerComponent] = self._player2.get_component(SkillControllerComponent)

    if skill_component is None:
      return

    drop_bomb_skill = skill_component._dromp_bomb_skill
    remaining_cdr: float = max(0.0, drop_bomb_skill._cdr - time.time() + drop_bomb_skill._last_use)

    remaining_cdr_image = self._cdr_font.render(f'{remaining_cdr:.2f}', True, (255, 255, 255))
    x = self.width() - self.height() - 2 * remaining_cdr_image.get_width()
    y = (self.height() - remaining_cdr_image.get_height()) / 2
    screen.blit(remaining_cdr_image, (x, y))

  def __draw_remainig_time(self, screen: pygame.Surface) -> None:
    remaining_time_image = self._font.render(f'{format_seconds_to_min_sec(self._remaining_time)}', True, (255, 255, 255))
    x = (self.width() - remaining_time_image.get_width()) / 2
    y = (self.height() - remaining_time_image.get_height()) / 2
    screen.blit(remaining_time_image, (x, y))

  def __draw_player1_lives(self, screen: pygame.Surface) -> None:
    player1_lives_image = self._font.render(str(self._player1._lives), True, (255, 255, 255))
    x = self.height()
    y = (self.height() - player1_lives_image.get_height()) / 2
    screen.blit(player1_lives_image, (x, y))

  def __draw_player2_lives(self, screen: pygame.Surface) -> None:
    player2_lives_image = self._font.render(str(self._player2._lives), True, (255, 255, 255))
    x = self.width() - self.height() - player2_lives_image.get_width()
    y = (self.height() - player2_lives_image.get_height()) / 2
    screen.blit(player2_lives_image, (x, y))
