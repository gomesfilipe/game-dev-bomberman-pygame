from typing import Dict, Optional, Callable, List
from src.core.game_object import GameObject
from src.commands.movement_commands import MovementCommands
from src.commands.skill_commands import SkillCommands
from src.enums.player_type_enum import PlayerTypeEnum
from src.sprites.player_sprites import PlayerSprites
from src.components.sprite_renderer_component import SpriteRendererComponent
from src.components.movement_controller_component import MovementControllerComponent
from src.components.skill_controller_component import SkillControllerComponent
from src.utils.player_status_manager import PlayerStatusManager
from typing import Tuple, Optional
from src.utils.utils import distance_from_points
import pygame
from src.enums.direction_enum import DirectionEnum
from config import PLAYER_MAX_LIVES
from src.enums.game_object_type_enum import GameObjectTypeEnum
from src.enums.event_enum import EventEnum

class PlayerGameObject(GameObject):
  def __init__(
      self,
      sprites: PlayerSprites,
      velocity: float,
      movement_commands: MovementCommands,
      skill_commands: SkillCommands,
      player_type: PlayerTypeEnum,
      lives: int,
      x: float,
      y: float,
      order_in_layer: int,
      game_object_type: GameObjectTypeEnum,
      name: str,
      layers: List[str] = [],
      min_x: float = -float('inf'),
      max_x: float = float('inf'),
      min_y: float = -float('inf'),
      max_y: float = float('inf'),
    ) -> None:
    super().__init__(sprites, x, y, order_in_layer, game_object_type, layers, min_x, max_x, min_y, max_y)
    self._sprites = sprites
    self._velocity = velocity
    self._lives = lives
    self._movement_commands = movement_commands
    self._skill_commands = skill_commands
    self._player_type = player_type
    self._name = name
    self._status_manager = PlayerStatusManager()

  def start(self) -> None:
    self._component_manager.add(SpriteRendererComponent, self)
    self._component_manager.add(MovementControllerComponent, self)
    self._component_manager.add(SkillControllerComponent, self)

    self._direction = DirectionEnum.DOWN
    self._current_sprite = self.__sprite_by_direction()
    self._alpha = 0.45

  @GameObject._update_decorator
  def update(self) -> None:
    if self._status_manager.dead.is_active():
      return

    if self._lives <= 0:
      self.death()
      return

    self._current_sprite = self.__sprite_by_direction()
    self._status_manager.update()

  def __sprite_by_direction(self) -> pygame.Surface:
    sprites = {
      DirectionEnum.UP: lambda: self._sprites.up(),
      DirectionEnum.LEFT: lambda: self._sprites.left(),
      DirectionEnum.DOWN: lambda: self._sprites.down(),
      DirectionEnum.RIGHT: lambda: self._sprites.right(),
    }

    sprite = sprites[self._direction]()

    if self._status_manager.immune.is_active():
      sprite = sprite.copy()
      sprite.set_alpha(128)

    return sprite

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

    self._x = self._previous_x
    self._y = self._previous_y

    closest_point, distance = self.__closest_point(other)

    if distance < self._alpha * self_l: # Corrige a posição de self
      closest_x, closest_y = closest_point
      self._x = closest_x - self_l / 2
      self._y = closest_y - self_h / 2
      self._previous_x = self._x
      self._previous_y = self._y

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
    self_y_center = self._y + self_h / 2

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

  def get_name(self) -> None:
    return self._name

  def take_damage(self) -> None:
    if not self._status_manager.immune.is_active():
      self._lives = max(0, self._lives - 1)
      self._status_manager.immune.set_active(True)

  def add_life(self) -> None:
    self._lives = min(self._lives + 1, PLAYER_MAX_LIVES)

  def death(self) -> None:
    self._status_manager.dead.set_active(True)
    movement_controller = self._component_manager.get(MovementControllerComponent)
    skill_controller = self._component_manager.get(SkillControllerComponent)
    self._component_manager.remove(movement_controller)
    self._component_manager.remove(skill_controller)

    if self._current_sprite in [self._sprites.up(), self._sprites.left(), self._sprites.left_dead()]:
      self._current_sprite = self._sprites.left_dead()
    elif self._current_sprite in [self._sprites.down(), self._sprites.right(), self._sprites.right_dead()]:
      self._current_sprite = self._sprites.right_dead()

    EventEnum.NEXT_SCENE.post_event()

  def get_lives(self) -> int:
    return self._lives

  def get_type(self) -> PlayerTypeEnum:
    return self._player_type
