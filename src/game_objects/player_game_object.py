from typing import Dict, Optional, Callable, List
from src.game_objects.game_object import GameObject
from src.utils.player_commands import PlayerCommands
from src.enums.player_type_enum import PlayerTypeEnum
from src.sprites.player_sprites import PlayerSprites
import math
from typing import Tuple, Optional
from src.utils.utils import lerp, distance_from_points
from src.scenes.scene import Scene
import time
import pygame

class PlayerGameObject(GameObject):
  def __init__(
      self,
      sprites: PlayerSprites,
      scene: Scene,
      delta_time: int,
      velocity: float,
      commands: PlayerCommands,
      player_type: PlayerTypeEnum,
      lives: int,
      x: float,
      y: float,
      order_in_layer: int,
      name: str,
      layers: List[str] = [],
    ) -> None:
    super().__init__(sprites, scene, x, y, order_in_layer, layers)
    self._sprites = sprites
    self._delta_time = delta_time
    self._velocity = velocity
    self._lives = lives
    self._commands = commands
    self._player_type = player_type
    self._name = name

    self._key_handlers = self.__key_handlers()

    self._theta: Optional[float] = None
    self._vx: Optional[float] = None
    self._vy: Optional[float] = None

  @GameObject._start_decorator
  def start(self) -> None:
    self._current_sprite = self._sprites.down()
    self._theta = 0.0
    self._previous_x = self._x
    self._previous_y = self._y
    self._alpha = 0.45

  def update(self) -> None:
    self.__handle_pressed_keys()

  def __vertical_move(self, angle: int) -> None:
    screen = self._scene.get_screen()
    display = self._scene.get_display()
    self._theta = math.radians(angle)
    self._vy = self._velocity * math.sin(self._theta)
    self._previous_y = self._y
    self._y = lerp(self._y + self._vy * self._delta_time, display.height(), screen.get_height() - self._sprites._hitbox.get_height())

  def __horizontal_move(self, angle: int) -> None:
    screen = self._scene.get_screen()
    self._theta = math.radians(angle)
    self._vx = self._velocity * math.cos(self._theta)
    self._previous_x = self._x
    self._x = lerp(self._x + self._vx * self._delta_time, 0, screen.get_width() - self._sprites._hitbox.get_width())

  def __move_up(self) -> None:
    self.__vertical_move(-90)
    self._current_sprite = self._sprites.up()

  def __move_down(self) -> None:
    self.__vertical_move(90)
    self._current_sprite = self._sprites.down()

  def __move_left(self) -> None:
    self.__horizontal_move(-180)
    self._current_sprite = self._sprites.left()

  def __move_right(self) -> None:
    self.__horizontal_move(0)
    self._current_sprite = self._sprites.right()

  def __key_handlers(self) -> Dict[str, Callable]:
    return {
      self._commands.up(): self.__move_up,
      self._commands.down(): self.__move_down,
      self._commands.left(): self.__move_left,
      self._commands.right(): self.__move_right,
    }

  def __handle_pressed_keys(self) -> None:
    pressed_keys = pygame.key.get_pressed()

    for key, handler in self._key_handlers.items():
      if pressed_keys[key]:
        handler()

  def on_collide(self, other: GameObject, layer: str) -> None:
    handlers: Dict[str, Callable] = {
      'player1_collision': lambda: self.__handle_block_layer(other),
      'player2_collision': lambda: self.__handle_block_layer(other),
    }

    if layer in handlers:
      handlers[layer]()

  def __handle_block_layer(self, other: GameObject) -> None:
    self_l: float = self._sprites._hitbox.get_width()
    self_h: float = self._sprites._hitbox.get_height()

    closest_point, distance = self.__closest_point(other)

    if distance < self._alpha * self_l: # Corrige a posição de self
      closest_x, closest_y = closest_point

      self._previous_x = self._x
      self._previous_y = self._y

      self._x = closest_x - self_l / 2
      self._y = closest_y - self_h / 2
    else: # Volta para a posição anterior
      self._x = self._previous_x
      self._y = self._previous_y

  # Pega os quatro pontos centrais da hitbox de self e identifica
  # o mais próximo e a distância.
  def __closest_point(self, other: GameObject) -> Tuple[Tuple[float, float], float]:
    other_l: float = other._sprites._hitbox.get_width()
    other_h: float = other._sprites._hitbox.get_height()

    self_l: float = self._sprites._hitbox.get_width()
    self_h: float = self._sprites._hitbox.get_height()

    other_x_center = other._x + other_l / 2
    other_y_center = other._y + other_h / 2

    self_x_center = self._x + self_l / 2
    self_y_center = self._y + other_h / 2

    dx = (other_l + self_l) / 2
    dy = (other_h + self_h) / 2

    points: List[Tuple[int, int]] = [
      (other_x_center - dx, other_y_center - dy),
      (other_x_center + dx, other_y_center - dy),
      (other_x_center - dx, other_y_center + dy),
      (other_x_center + dx, other_y_center + dy),
    ]

    minn = float('inf')
    closest_point: Optional[Tuple[int, int]] = None

    for point in points:
      distance = distance_from_points(point, (self_x_center, self_y_center))

      if distance < minn:
        minn = distance
        closest_point = point

    return closest_point, minn

  def get_lives(self) -> int:
    return self._lives

  def set_lives(self, lives: int) -> None:
    self._lives = lives

  def get_name(self) -> None:
    return self._name
