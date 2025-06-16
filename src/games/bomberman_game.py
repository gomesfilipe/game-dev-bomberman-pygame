from src.core.game import Game
from src.core.scene import Scene
from src.scenes.main_scene import MainScene
from src.scenes.choose_players_scene import ChoosePlayersScene
from src.scenes.winner_scene import WinnerScene
from config import SCREEN, GAME_DURATION, TILES_WIDTH, TILES_HEIGHT
from typing import Dict, Tuple, Optional, Callable


class BombermanGame(Game):
  def __init__(self):
    background_color: str = 'wheat3'

    self.__choose_players_scene = ChoosePlayersScene(SCREEN.get_width(), SCREEN.get_height(), TILES_WIDTH, TILES_HEIGHT, background_color)
    self.__main_scene = MainScene(SCREEN.get_width(), SCREEN.get_height(), TILES_WIDTH, TILES_HEIGHT, GAME_DURATION, background_color)
    self.__winner_scene = WinnerScene(SCREEN.get_width(), SCREEN.get_height(), TILES_WIDTH, TILES_HEIGHT, background_color)

    super().__init__(SCREEN)

  def _scenes_order(self) -> Dict[Scene, Tuple[Optional[Scene], Optional[Callable[[Scene, Scene], None]]]]:
    return {
      self.__choose_players_scene: (self.__main_scene, lambda src_scene, target_scene: self.__choose_2_main_scene(src_scene, target_scene)),
      self.__main_scene: (self.__winner_scene, lambda src_scene, target_scene: self.__main_2_winner_scene(src_scene, target_scene)),
      self.__winner_scene: (self.__choose_players_scene, lambda src_scene, target_scene: self.__winner_2_choose_scene(src_scene, target_scene)),
    }

  def _initial_scene(self) -> Scene:
    return self.__choose_players_scene

  def __choose_2_main_scene(self, choose_players_scene: ChoosePlayersScene, main_scene: MainScene) -> None:
    player1_type = choose_players_scene.current_player1_type()
    player2_type = choose_players_scene.current_player2_type()
    main_scene.set_player_types(player1_type, player2_type)

  def __main_2_winner_scene(self, main_scene: MainScene, winner_scene: WinnerScene) -> None:
    winner_player_type = main_scene.get_winner_player_type()
    winner_scene.set_winner_player_type(winner_player_type)

  def __winner_2_choose_scene(self, winner_scene: WinnerScene, choose_players_scene: ChoosePlayersScene) -> None:
    return
