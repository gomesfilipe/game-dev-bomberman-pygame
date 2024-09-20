from typing import List, Optional, Dict, Callable
from src.core.scene import Scene
import pygame
from config import *
from src.enums.player_type_enum import PlayerTypeEnum
from src.core.game_events import GameEvents
from src.enums.event_enum import EventEnum

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
    self._button_height: int = 80
    self._button_width: int = 100
    self._logo_height: int = 60
    self._sprites_size: int = 256
    self._player_types: List[PlayerTypeEnum] = PlayerTypeEnum.cases()

    self._sprites = [
      player_type.single_sprite(self._sprites_size, self._sprites_size) for player_type in self._player_types
    ]

    self._player1_selected_index: int = 0
    self._player2_selected_index: int = 1

    self._click_handlers = self.__click_handlers()

  def _draw_rectangle(
    self,
    screen: pygame.Surface,
    x: float,
    y: float,
    width: int,
    height: int,
    text: str,
    font: Optional[pygame.font.Font] = None
  ) -> pygame.Rect:
    if font is None:
      font = self._font

    rect = pygame.draw.rect(screen, 'black', (x, y, width, height))

    text_image = font.render(f'{text}', True, (255, 255, 255))
    x_image = x + (width - text_image.get_width()) / 2
    y_image = y + (height - text_image.get_height()) / 2
    screen.blit(text_image, (x_image, y_image))

    return rect

  def _current_player1_sprite(self) -> SimpleSprite:
    return self._sprites[self._player1_selected_index]

  def _current_player2_sprite(self) -> SimpleSprite:
    return self._sprites[self._player2_selected_index]

  def current_player1_type(self) -> PlayerTypeEnum:
    return self._player_types[self._player1_selected_index]

  def current_player2_type(self) -> PlayerTypeEnum:
    return self._player_types[self._player2_selected_index]

  def _next_player1_index(self) -> None:
    fn_next_index = lambda: (self._player1_selected_index + 1) % len(self._player_types)
    self._player1_selected_index = fn_next_index()

    if self._player1_selected_index == self._player2_selected_index:
      self._player1_selected_index = fn_next_index()

  def _next_player2_index(self) -> None:
    fn_next_index = lambda: (self._player2_selected_index + 1) % len(self._player_types)
    self._player2_selected_index = fn_next_index()

    if self._player2_selected_index == self._player1_selected_index:
      self._player2_selected_index = fn_next_index()

  def start(self) -> None:
    self._font: pygame.font.Font = pygame.font.SysFont('impact', 48)
    self._smaller_font: pygame.font.Font = pygame.font.SysFont('impact', 32)
    self._player1_button: Optional[pygame.rect.Rect] = None
    self._player2_button: Optional[pygame.rect.Rect] = None
    self._start_button: Optional[pygame.rect.Rect] = None

  def update(self) -> None:
    self.__handle_click()

  def draw(self, screen: pygame.Surface) -> None:
    screen.fill(self._background_color)

    if self._display is not None:
      self._display.draw(screen)

    self.__draw_title(screen)
    self.__draw_selected_player1(screen)
    self.__draw_selected_player2(screen)
    self.__draw_start_button(screen)
    self.__draw_player1_button(screen)
    self.__draw_player2_button(screen)

    pygame.display.flip()

  def __draw_title(self, screen: pygame.Surface) -> None:
    title: str = 'Bomberman: Animal Revolution'
    self._draw_rectangle(screen, 0, 0, screen.get_width(), self._logo_height, title)

  def __draw_selected_player1(self, screen: pygame.Surface) -> None:
    sprite = self._current_player1_sprite()
    screen.blit(sprite.idle(), (0, (screen.get_height() - sprite.height()) / 2))

  def __draw_selected_player2(self, screen: pygame.Surface) -> None:
    sprite = self._current_player2_sprite()
    flipped_sprite = pygame.transform.flip(sprite.idle(), True, False)
    screen.blit(flipped_sprite, (screen.get_width() - sprite.width(), (screen.get_height() - sprite.height()) / 2))

  def __draw_start_button(self, screen: pygame.Surface) -> None:
    title: str = 'Start Game'
    width: int = screen.get_width() / 2
    height: int = self._logo_height

    self._start_button = self._draw_rectangle(screen, (screen.get_width() - width) / 2, screen.get_height() - height, width, height, title)

  def __draw_player1_button(self, screen: pygame.Surface) -> None:
    text: str = self.current_player1_type().value
    self._player1_button = self._draw_rectangle(screen, 45, 120, screen.get_width() / 3, 30, text, self._smaller_font)

  def __draw_player2_button(self, screen: pygame.Surface) -> None:
    text: str = self.current_player2_type().value
    width: int = screen.get_width() / 3

    self._player2_button = self._draw_rectangle(screen, screen.get_width() - 45 - width, 120, width, 30, text, self._smaller_font)

  def __click_handlers(self) -> Dict[int, Callable]:
    return {
      pygame.BUTTON_LEFT: lambda: self.__handle_left_click(),
    }

  def __handle_left_click(self) -> None:
    x, y = pygame.mouse.get_pos()

    if self._player1_button.collidepoint(x, y):
      self._next_player1_index()
    elif self._player2_button.collidepoint(x, y):
      self._next_player2_index()
    elif self._start_button.collidepoint(x, y):
      EventEnum.NEXT_SCENE.post_event()

  def __handle_click(self) -> None:
    event = GameEvents.find(lambda event: event.type == pygame.MOUSEBUTTONDOWN)
    if event is None:
      return

    if  event.button in self._click_handlers:
      self._click_handlers[event.button]()
