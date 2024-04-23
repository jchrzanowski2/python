import pygame
from constants import Constants
from world import World, make_world
from world_objects import SpriteGroups
from bullet import Bullet

pygame.init()

SCREEN_WIDTH = Constants.SCREEN_WIDTH
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

moving_left = False
moving_right = False
shoot = False

clock = pygame.time.Clock()


# colors
def draw_bg() -> None:
    screen.fill(Constants.BG)


font = pygame.font.Font(None, 36)

player, world, groups = make_world()

start_time = pygame.time.get_ticks()

finish = 120


def show_game_info(player):
    elapsed_time = pygame.time.get_ticks() - start_time
    elapsed_text = font.render(
        "Elapsed Time: {} h {} min {} s".format(
            elapsed_time // 3600000,
            elapsed_time // 60000 % 60,
            elapsed_time // 1000 % 60,
        ),
        True,
        Constants.BLACK,
    )
    screen.blit(elapsed_text, (10, 10))

    points_text = font.render(
        "Points: {}".format(player.points),
        True,
        Constants.BLACK
    )
    screen.blit(points_text, (600, 10))

    health = font.render(
        "Health: {}".format(
        player.health
        ),
        True,
        Constants.BLACK
    )
    screen.blit(health, (10, 40))



run = True
while run:

    clock.tick(Constants.FPS)

    draw_bg()

    world.draw(screen, Constants.screen_scroll)

    player.update(player.rect)
    player.draw(screen, player.rect)

    Constants.bullet_group.update(player)
    Constants.bullet_group.draw(screen)

    for enemy in Constants.enemy_group:
        enemy.ai(world.obstacle_list, player)
        enemy.update(player.rect)
        enemy.draw(screen, player.rect)

    if player.alive:
        if shoot:
            player.shoot()
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
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_w and not player.in_air and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False

    world.groups.update_draw(screen, player, world)
    if world.stop: run = False
    if not player.alive:
        if finish:
            finish -= 1
        else:
            run = False

    show_game_info(player)

    pygame.display.update()

pygame.quit()
