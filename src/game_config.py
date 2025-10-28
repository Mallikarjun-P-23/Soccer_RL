"""
Game Configuration Module
Contains all game constants, initialization settings, and color definitions.
"""

import pygame
import random

# Initialize pygame
print("Initializing pygame...")
pygame.init()
print("Pygame initialized successfully")

# Screen setup
WIDTH, HEIGHT = 1000, 600
print(f"Creating display window {WIDTH}x{HEIGHT}...")
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RoboSoccer - 2v2")
    print("Display window created successfully!")
    print("\n" + "="*60)
    print("📊 REPORT GENERATION INSTRUCTIONS")
    print("="*60)
    print("To generate performance reports:")
    print("  1. Press 'E' key anytime during the game")
    print("  2. Or play for 3 minutes / Press 'Q' key")
    print("Reports will be saved to 'reports/' folder")
    print("="*60 + "\n")
except Exception as e:
    print(f"Error creating display: {e}")
    import sys
    sys.exit(1)

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 100, 255)
RED = (255, 50, 50)
GREEN = (50, 180, 50)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
DARK_GREEN = (0, 150, 0)
LIGHT_GREEN = (100, 200, 100)
GRAY = (150, 150, 150)
DARK_GRAY = (50, 50, 50)
BROWN = (139, 69, 19)
SKIN = (240, 200, 150)
LIGHT_BLUE = (135, 206, 250)

# Game objects dimensions
BALL_RADIUS = 15
PLAYER_RADIUS = 18
PLAYER_SPEED = 4
BALL_SPEED = 5
FRICTION = 0.98

# Stadium dimensions
FIELD_WIDTH, FIELD_HEIGHT = 800, 450
FIELD_X, FIELD_Y = (WIDTH - FIELD_WIDTH) // 2, (HEIGHT - FIELD_HEIGHT) // 2

# Game timing
goal_delay = 60  # frames to wait after goal

# Fonts
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 24)
large_font = pygame.font.SysFont(None, 72)

# Audience setup
def create_audience():
    """Create audience members around the stadium"""
    audience = []
    for i in range(150):
        x = random.randint(0, WIDTH)
        y = random.randint(0, FIELD_Y - 20)
        color = random.choice([RED, BLUE, WHITE, YELLOW, BROWN, SKIN, LIGHT_BLUE])
        audience.append((x, y, color, random.choice([0, 1, 2])))

    for i in range(150):
        x = random.randint(0, WIDTH)
        y = random.randint(FIELD_Y + FIELD_HEIGHT + 10, HEIGHT)
        color = random.choice([RED, BLUE, WHITE, YELLOW, BROWN, SKIN, LIGHT_BLUE])
        audience.append((x, y, color, random.choice([0, 1, 2])))
    
    return audience

# Cheering sound - disabled to prevent annoying noise
try:
    cheer_sound = None  # Disabled random sound generation
except:
    cheer_sound = None

# Clock for frame rate control
clock = pygame.time.Clock()