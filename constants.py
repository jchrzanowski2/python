import pygame
from pygame import mixer


# Struct with all constants for easy editing
class Constants:
    """Class containing various constants used in the game."""

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

    ROWS = 16
    COLS = 150

    TILE_SIZE = SCREEN_HEIGHT // ROWS
    TILE_TYPES = 22

    BG = (200, 200, 200)  # background colors
    FPS = 60

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (128, 128, 128)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    ORANGE = (255, 128, 0)
    DARK_GREY = (70, 70, 70)

    class Actions:
        """Class containing game action constants."""
        GAME_END = 1
        GAME_START = 2

    KILL = 100
    KILL_RED = 101
    KILL_PURPLE = 102
    GRAVITY = 0.75
    SCROLL_THRESH = 200
    screen_scroll = 0
    bg_scroll = 0
    LEVEL_NUM = 2
    
    enemy_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()

    high_score_file = 'high_score.json'


class PlayerActions:
    """Class containing player action flags."""
    moving_left = False
    moving_right = False
    shoot = False


class Statistics:
    """Class containing player statistics."""
    time = 0
    points = 0
    bullets_shot = 0
    distance_travelled = 0
    kills = 0
    total_points = 0


class SoundEffect:
    """Class containing sound effects for the game."""
    mixer.init()
    jump_fx = pygame.mixer.Sound("audio/jump.wav")
    jump_fx.set_volume(0.2)
    shot_fx = pygame.mixer.Sound("audio/shot.wav")
    shot_fx.set_volume(0.2)
