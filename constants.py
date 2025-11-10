"""
Galaga Game Constants
Based on the original Namco Galaga arcade game
"""

# Screen dimensions (original was 224x288, scaled up for modern displays)
SCREEN_WIDTH = 672  # 224 * 3
SCREEN_HEIGHT = 864  # 288 * 3
SCALE = 3

# Colors (classic Galaga palette)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 112, 221)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (170, 0, 170)
CYAN = (0, 255, 255)

# Game settings
FPS = 60
PLAYER_SPEED = 4
BULLET_SPEED = 8
ENEMY_BULLET_SPEED = 6

# Player settings
PLAYER_WIDTH = 13 * SCALE
PLAYER_HEIGHT = 16 * SCALE
PLAYER_START_LIVES = 3
PLAYER_Y_POSITION = SCREEN_HEIGHT - 100

# Enemy settings
ENEMY_WIDTH = 12 * SCALE
ENEMY_HEIGHT = 12 * SCALE
FORMATION_TOP_Y = 120
FORMATION_START_X = 150
FORMATION_SPACING_X = 48
FORMATION_SPACING_Y = 48

# Enemy types
ENEMY_BEE = 'bee'
ENEMY_BUTTERFLY = 'butterfly'
ENEMY_BOSS = 'boss'

# Scoring (original Galaga scoring)
SCORE_BEE = 50
SCORE_BUTTERFLY = 80
SCORE_BOSS = 150
SCORE_BOSS_DIVING = 400
SCORE_CAPTURED_FIGHTER = 500
SCORE_DUAL_FIGHTER_BONUS = 1000

# Stages
ENEMIES_PER_STAGE = 40
STAGE_CLEAR_DELAY = 2000  # milliseconds

# Attack patterns
DIVE_SPEED = 3
DIVE_CURVE_STRENGTH = 2
FORMATION_SWAY_SPEED = 0.5
FORMATION_SWAY_AMOUNT = 20

# Capture beam settings
CAPTURE_BEAM_WIDTH = 20
CAPTURE_BEAM_SPEED = 4
CAPTURE_BEAM_LENGTH = 60

# Game states
STATE_TITLE = 'title'
STATE_PLAYING = 'playing'
STATE_STAGE_START = 'stage_start'
STATE_GAME_OVER = 'game_over'
STATE_BONUS_STAGE = 'bonus_stage'
