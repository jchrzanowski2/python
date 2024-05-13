import pygame
from constants import Constants
from game_manager import GameManager
from observer import Observer

pygame.init()

SCREEN_WIDTH = Constants.SCREEN_WIDTH
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

clock = pygame.time.Clock()

# colors
def draw_bg() -> None:
    screen.fill(Constants.BG)

game = GameManager()
observer = Observer()
game.current_state.attach(observer)

run = True
while run:

    clock.tick(Constants.FPS)

    draw_bg()

    game.update()
    game.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        else:
            game.handle_events(event)

    if observer.action:
        observer.act(game)
        game.current_state.attach(observer)
    
    observer.pass_info(game)

    pygame.display.update()

pygame.quit()
