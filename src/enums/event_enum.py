from enum import Enum
import pygame

class EventEnum(Enum):
  COLLISION = pygame.USEREVENT + 1
  QUIT = pygame.QUIT
