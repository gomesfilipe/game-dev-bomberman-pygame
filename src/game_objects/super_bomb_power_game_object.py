from typing import Tuple, Callable, Dict, Optional
from src.core.game_object import GameObject
from src.game_objects.player_game_object import PlayerGameObject
from src.game_objects.power_game_object import PowerGameObject
from src.sprites.simple_sprite import SimpleSprite
from os.path import join
from src.enums.power_enum import PowerEnum
from src.components.skill_controller_component import SkillControllerComponent
from config import SUPER_BOMB_POWER_SPRITE
from src.enums.game_object_type_enum import GameObjectTypeEnum

class SuperBombPowerGameObject(PowerGameObject):
  def __init__(
      self,
      x: float,
      y: float,
      size: Tuple[int, int],
      game_object_type: GameObjectTypeEnum,
      min_x: float = -float('inf'),
      max_x: float = float('inf'),
      min_y: float = -float('inf'),
      max_y: float = float('inf'),
    ) -> None:
    super().__init__(x, y, size, game_object_type, PowerEnum.SUPER_BOMB, min_x, max_x, min_y, max_y)

  def on_collide(self, other: GameObject, layer: str) -> None:
    handlers: Dict[str, Callable] = {
      'player1_power': lambda: self.__handle_power_layer(other),
      'player2_power': lambda: self.__handle_power_layer(other),
    }
    if layer in handlers:
      handlers[layer]()

  def _define_sprites(self) -> SimpleSprite:
    return SUPER_BOMB_POWER_SPRITE

  def __handle_power_layer(self, other: PlayerGameObject) -> None:
    skill_component: Optional[SkillControllerComponent] = other.get_component(SkillControllerComponent)

    if skill_component is not None:
      drop_bomb_skill = skill_component._dromp_bomb_skill
      drop_bomb_skill.set_super_bomb()

    self.destroy()
