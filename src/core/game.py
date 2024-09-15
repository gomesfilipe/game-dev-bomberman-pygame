import pygame
from typing import Dict, Callable
from src.core.scene import Scene
from src.enums.event_enum import EventEnum
from src.core.game_time import GameTime
from src.core.game_events import GameEvents

class Game():
  def __init__(
      self,
      screen: pygame.Surface,
      scene: Scene,
    ) -> None:
    self._screen = screen
    self._scene = scene
    self._stop: bool = False

    self._event_handlers = self._get_event_handlers()
    self._key_handlers = self._get_key_handlers()

  def _should_stop(self) -> None:
    return self._stop

  def _get_event_handlers(self) -> Dict[int, Callable]:
    return {
      EventEnum.QUIT.value: lambda event: self.__handle_quit_event(event),
      EventEnum.PRESSED_KEY.value: lambda event: self.__handle_pressed_key_event(event),
      EventEnum.NEW_GAME_OBJECT.value: lambda event: self.__handle_new_game_object_event(event),
      EventEnum.DESTROY_GAME_OBJECT.value: lambda event: self.__handle_destroy_game_object_event(event),
    }

  def _get_key_handlers(self) -> Dict[int, Callable]:
    return {
      pygame.K_SPACE: lambda: self._scene.switch_debug_mode(),
    }

  def __handle_quit_event(self, event: pygame.event.Event) -> None:
    self._stop = True

  def __handle_pressed_key_event(self, event: pygame.event.Event) -> None:
    if event.key in self._key_handlers:
      self._key_handlers[event.key]()

  def __handle_new_game_object_event(self, event: pygame.event.Event) -> None:
    self._scene.add_game_object(event.game_object)

  def __handle_destroy_game_object_event(self, event: pygame.event.Event) -> None:
    self._scene.remove_game_object(event.game_object)

  def run(self):
    pygame.init()
    self._scene.start()

    while not self._should_stop():
      GameTime.update()

      i: int = 0
      while GameTime.has_physics_time():
        self.__handle_events()
        self._scene.update()
        GameTime.fixed_update()
        i += 1

      if i > 0:
        self._scene.draw(self._screen)
      GameTime.wait_fps()

    pygame.quit()

  def __handle_events(self) -> None:
    GameEvents.update()
    events = GameEvents.get(lambda event: event.type in self._event_handlers)

    for event in events:
      self._event_handlers[event.type](event)

  def set_scene(self, scene: Scene) -> None:
    self._scene = scene
