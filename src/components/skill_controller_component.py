from src.core.component import Component
from typing import Dict, Callable
from src.commands.skill_commands import SkillCommands
from src.skills.drop_bomb_skill import DropBombSkill
from src.core.game_events import GameEvents

class SkillControllerComponent(Component):
  pass

from src.core.game_object import GameObject
import pygame

class SkillControllerComponent(Component):
  def __init__(self, game_object: GameObject, name: str = ''):
    super().__init__(game_object, name)
    self._dromp_bomb_skill = DropBombSkill()

    if self._game_object._movement_commands is None:
      self._commands = SkillCommands(pygame.K_p)
    else:
      self._commands = self._game_object._skill_commands

    self._key_handlers = self.__key_handlers()

  def draw(self, screen: pygame.Surface):
    return

  def start(self) -> None:
    return

  def update(self) -> None:
    self.__handle_down_key()

  def fixed_update(self) -> None:
    return

  def __key_handlers(self) -> Dict[str, Callable]:
    return {
      self._commands.drop_bomb(): lambda: self._dromp_bomb_skill.execute(self._game_object),
    }

  def __handle_down_key(self) -> None:
    event = GameEvents.find(lambda event: event.type == pygame.KEYDOWN)

    if event is None:
      return

    if event.key in self._key_handlers:
      self._key_handlers[event.key]()
