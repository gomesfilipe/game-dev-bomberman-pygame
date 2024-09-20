from typing import List, Optional, Dict, Callable
from src.core.scene import Scene
import pygame
from config import *
from src.sprites.simple_sprite import SimpleSprite
from src.enums.player_type_enum import PlayerTypeEnum
from src.core.game_events import GameEvents
from src.enums.event_enum import EventEnum

class WinnerScene(Scene):
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

    self._winner_player_type: Optional[PlayerTypeEnum] = None
    self._sprite: Optional[PlayerSprites] = None

    self._player1_selected_index: int = 0
    self._player2_selected_index: int = 1

    self._click_handlers = self.__click_handlers()

  def set_winner_player_type(self, player_type: PlayerTypeEnum) -> None:
    self._winner_player_type = player_type
    self._sprite = self._winner_player_type.sprites(self._sprites_size, self._sprites_size)

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

  def start(self) -> None:
    self._font: pygame.font.Font = pygame.font.SysFont('impact', 48)
    self._play_again_button: Optional[pygame.rect.Rect] = None

  def update(self) -> None:
    self.__handle_click()

  def draw(self, screen: pygame.Surface) -> None:
    screen.fill(self._background_color)

    if self._display is not None:
      self._display.draw(screen)

    self.__draw_title(screen)
    self.__draw_winner(screen)
    self.__draw_play_again_button(screen)

    pygame.display.flip()

  def __draw_title(self, screen: pygame.Surface) -> None:
    if self._winner_player_type is None:
      title: str = 'There is no winner!'
    else:
      title: str = f'Winner: {self._winner_player_type.value}'

    self._draw_rectangle(screen, 0, 0, screen.get_width(), self._logo_height, title)

  def __draw_winner(self, screen: pygame.Surface) -> None:
    if self._winner_player_type is None:
      return

    sprite = self._winner_player_type.single_sprite(self._sprites_size, self._sprites_size)
    screen.blit(sprite.idle(), ((screen.get_width() - sprite.width()) / 2, (screen.get_height() - sprite.height()) / 2))

  def __draw_play_again_button(self, screen: pygame.Surface) -> None:
    title: str = 'Play Again'
    width: int = screen.get_width() / 2
    height: int = self._logo_height

    self._play_again_button = self._draw_rectangle(screen, (screen.get_width() - width) / 2, screen.get_height() - height, width, height, title)

  def __click_handlers(self) -> Dict[int, Callable]:
    return {
      pygame.BUTTON_LEFT: lambda: self.__handle_left_click(),
    }

  def __handle_left_click(self) -> None:
    x, y = pygame.mouse.get_pos()

    if self._play_again_button.collidepoint(x, y):
      EventEnum.NEXT_SCENE.post_event()

  def __handle_click(self) -> None:
    event = GameEvents.find(lambda event: event.type == pygame.MOUSEBUTTONDOWN)
    if event is None:
      return

    if  event.button in self._click_handlers:
      self._click_handlers[event.button]()
