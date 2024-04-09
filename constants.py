import pygame


# Struct with all constants for easy editing
class Constants:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

    ROWS = 16
    COLS = 150

    TILE_SIZE = SCREEN_HEIGHT // ROWS
    TILE_TYPES = 21

    BG = (200, 200, 200)  # background colors
    FPS = 60

    GRAVITY = 0.75
    SCROLL_THRESH = 200
    screen_scroll = 0
    bg_scroll = 0

    enemy_group = pygame.sprite.Group()
