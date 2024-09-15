from src.core.game import Game
from src.scenes.main_scene import MainScene
from typing import Tuple, List
import pygame
from config import *

if __name__ == '__main__':
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  scene = MainScene(screen.get_width(), screen.get_height(), GAME_DURATION, 'wheat3')

  game = Game(screen, scene)
  game.run()
