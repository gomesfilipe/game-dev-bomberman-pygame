from src.core.game import Game
from src.scenes.main_scene import MainScene
from src.scenes.choose_players_scene import ChoosePlayersScene
import pygame
from config import SCREEN, GAME_DURATION, TILES_WIDTH, TILES_HEIGHT

if __name__ == '__main__':
  # scene = MainScene(SCREEN.get_width(), SCREEN.get_height(), TILES_WIDTH, TILES_HEIGHT, GAME_DURATION, 'wheat3')
  # game = Game(SCREEN, scene)

  choose_players_scene = ChoosePlayersScene(SCREEN.get_width(), SCREEN.get_height(), TILES_WIDTH, TILES_HEIGHT, 'wheat3')
  game = Game(SCREEN, choose_players_scene)
  game.run()
