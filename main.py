import pygame
from constants import Constants
from world import World, make_world
from world_objects import SpriteGroups

pygame.init()

SCREEN_WIDTH = Constants.SCREEN_WIDTH
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

moving_left = False
moving_right = False

clock = pygame.time.Clock()


# colors
def draw_bg() -> None:
    screen.fill(Constants.BG)


player, world, groups = make_world()

run = True
while run:

    clock.tick(Constants.FPS)

    draw_bg()

    world.draw(screen, Constants.screen_scroll)

    player.update_animation()
    player.draw(screen)

    for enemy in Constants.enemy_group:
        enemy.ai(world.obstacle_list)
        enemy.update_animation()
        enemy.draw(screen)

    if player.alive:
        if player.in_air:
            player.update_action(2)
        elif moving_left or moving_right:
            player.update_action(1)
        else:
            player.update_action(0)
        Constants.screen_scroll = player.move(
            moving_left, moving_right, world.obstacle_list
        )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and not player.in_air and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    groups.update_draw(screen, screen_scroll)

    pygame.display.update()

pygame.quit()
