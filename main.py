from src.core.game import Game
from src.scenes.main_scene import MainScene
from src.scenes.choose_players_scene import ChoosePlayersScene
import pygame
from config import SCREEN, GAME_DURATION, TILES_WIDTH, TILES_HEIGHT

def choose_2_main_scene(choose_players_scene: ChoosePlayersScene, main_scene: MainScene) -> None:
  player1_type = choose_players_scene.current_player1_type()
  player2_type = choose_players_scene.current_player2_type()
  main_scene.set_player_types(player1_type, player2_type)

if __name__ == '__main__':
  choose_players_scene = ChoosePlayersScene(SCREEN.get_width(), SCREEN.get_height(), TILES_WIDTH, TILES_HEIGHT, 'wheat3')
  main_scene = MainScene(SCREEN.get_width(), SCREEN.get_height(), TILES_WIDTH, TILES_HEIGHT, GAME_DURATION, 'wheat3')

  scenes_order = {
    choose_players_scene: (main_scene, lambda src_scene, target_scene: choose_2_main_scene(src_scene, target_scene))
  }

  game = Game(SCREEN, choose_players_scene, scenes_order)
  game.run()
