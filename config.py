from src.enums.player_type_enum import PlayerTypeEnum

PLAYER_1_TYPE: PlayerTypeEnum = PlayerTypeEnum.PIG
PLAYER_2_TYPE: PlayerTypeEnum = PlayerTypeEnum.RABBIT

PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64

PLAYER_1_NAME = 'player1'
PLAYER_2_NAME = 'player2'

PLAYER_VELOCITY: float = 100
PLAYER_MAX_LIVES: int = 5

PLAYER_GAME_OBJECT_ORDER_IN_LAYER = 2
POWER_GAME_OBJECT_ORDER_IN_LAYER = 1
BLOCK_GAME_OBJECT_ORDER_IN_LAYER = 0

BLOCK_SIZE: int = 32
DISPLAY_HEIGHT: int = 80

GAME_DURATION: int = 300

SCREEN_WIDTH: int = BLOCK_SIZE * 15
SCREEN_HEIGHT: int = DISPLAY_HEIGHT + BLOCK_SIZE * 11

PROBABILITY_SPAWN_POWER: float = 0.5
