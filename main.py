import pygame
from character import Character

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Game')

moving_left = False
moving_right = False

clock = pygame.time.Clock()
FPS = 60

#colors
BG = (200, 200, 200)

def draw_bg():
    screen.fill(BG)


player = Character('player', 200, 400, 3, 5)

run = True
while run:

    clock.tick(FPS)
    draw_bg()
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

    pygame.display.update()


pygame.quit()