from typing import Dict, Optional, Callable, List
from src.core.game_object import GameObject
from src.utils.movement_commands import MovementCommands
from src.enums.player_type_enum import PlayerTypeEnum
from src.sprites.player_sprites import PlayerSprites
from src.components.sprite_renderer_component import SpriteRendererComponent
from src.components.movement_controller_component import MovementControllerComponent
from typing import Tuple, Optional
from src.utils.utils import distance_from_points
import pygame
from src.core.display import Display
from src.enums.direction_enum import DirectionEnum
class PlayerGameObject(GameObject):
  def __init__(
      self,
      screen: pygame.Surface,
      display: Display,
      sprites: PlayerSprites,
      delta_time: float,
      velocity: float,
      commands: MovementCommands,
      player_type: PlayerTypeEnum,
      lives: int,
      x: float,
      y: float,
      order_in_layer: int,
      name: str,
      layers: List[str] = [],
    ) -> None:
    super().__init__(screen, display, sprites, x, y, order_in_layer, layers)
    self._sprites = sprites
    self._delta_time = delta_time
    self._velocity = velocity
    self._lives = lives
    self._commands = commands
    self._player_type = player_type
    self._name = name

  @GameObject._start_decorator
  def start(self) -> None:
    self._component_manager.add(SpriteRendererComponent, self)
    self._component_manager.add(MovementControllerComponent, self)

    self._direction = DirectionEnum.DOWN
    self._current_sprite = self.__sprite_by_direction()
    self._alpha = 0.45

  @GameObject._update_decorator
  def update(self) -> None:
    if self._lives <= 0:
      self.destroy()
      return

    self._current_sprite = self.__sprite_by_direction()

  def __sprite_by_direction(self) -> pygame.Surface:
    sprites = {
      DirectionEnum.UP: lambda: self._sprites.up(),
      DirectionEnum.LEFT: lambda: self._sprites.left(),
      DirectionEnum.DOWN: lambda: self._sprites.down(),
      DirectionEnum.RIGHT: lambda: self._sprites.right(),
    }

    return sprites[self._direction]()

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
