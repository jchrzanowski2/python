import pygame
from world import World, make_world
from constants import Constants
from world_objects import SpriteGroups

pygame.init()

SCREEN_WIDTH = Constants.SCREEN_WIDTH
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Game')

moving_left = False
moving_right = False

clock = pygame.time.Clock()

#colors
def draw_bg() -> None:
    screen.fill(Constants.BG)

player, world, groups = make_world()

run = True
while run:

    clock.tick(Constants.FPS)

    draw_bg()

    world.draw(screen)

    player.draw(screen)

    player.move(moving_left, moving_right)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    groups.update_draw(screen)

    pygame.display.update()


pygame.quit()   