from src.core.game import Game
from src.scenes.main_scene import MainScene
from src.scenes.choose_players_scene import ChoosePlayersScene
from src.scenes.winner_scene import WinnerScene
from config import SCREEN, GAME_DURATION, TILES_WIDTH, TILES_HEIGHT

def choose_2_main_scene(choose_players_scene: ChoosePlayersScene, main_scene: MainScene) -> None:
  player1_type = choose_players_scene.current_player1_type()
  player2_type = choose_players_scene.current_player2_type()
  main_scene.set_player_types(player1_type, player2_type)

def main_2_winner_scene(main_scene: MainScene, winner_scene: WinnerScene) -> None:
  winner_player_type = main_scene.get_winner_player_type()
  winner_scene.set_winner_player_type(winner_player_type)

def winner_2_choose_scene(winner_scene: WinnerScene, choose_players_scene: ChoosePlayersScene) -> None:
  return

if __name__ == '__main__':
  background_color: str = 'wheat3'

  choose_players_scene = ChoosePlayersScene(SCREEN.get_width(), SCREEN.get_height(), TILES_WIDTH, TILES_HEIGHT, background_color)
  main_scene = MainScene(SCREEN.get_width(), SCREEN.get_height(), TILES_WIDTH, TILES_HEIGHT, GAME_DURATION, background_color)
  winner_scene = WinnerScene(SCREEN.get_width(), SCREEN.get_height(), TILES_WIDTH, TILES_HEIGHT, background_color)

  # Gerencia a ordem das cenas e passagem de informação entre elas.
  scenes_order = {
    choose_players_scene: (main_scene, lambda src_scene, target_scene: choose_2_main_scene(src_scene, target_scene)),
    main_scene: (winner_scene, lambda src_scene, target_scene: main_2_winner_scene(src_scene, target_scene)),
    winner_scene: (choose_players_scene, lambda src_scene, target_scene: winner_2_choose_scene(src_scene, target_scene)),
  }

  game = Game(SCREEN, choose_players_scene, scenes_order)
  game.run()
