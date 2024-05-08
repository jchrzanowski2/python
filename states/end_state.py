import pygame
from .game_state import GameState
from constants import Constants

pygame.font.init()
font = pygame.font.Font(None, 36)

def make_surface(
        text: str, 
        position: tuple[int, int], 
        *, to_left: bool = False
) -> tuple[pygame.Surface, pygame.Rect]:
    text_surface = font.render(text, True, Constants.BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = position
    if to_left: text_rect.left = position[0]

    return text_surface, text_rect

class EndState(GameState):
    def __init__(self, win: bool, time_played: int, points: int) -> None:
        super().__init__()
        self.won = "won" if win else "lost"
        self.time = time_played
        self.texts: list[tuple[pygame.Surface, pygame.Rect]] = []
        self.points = points
        self.add_texts()

    def draw(self, screen: pygame.Surface) -> None:
        for surface, rect in self.texts:
            screen.blit(surface, rect)
    
    def update(self) -> None:
        return super().update()
    
    def handle_events(self, event: pygame.event.Event) -> None:
        return super().handle_events(event)
    
    def add_texts(self):
        self.texts.append(
            make_surface("You {}!".format(self.won), (400, 100))
            ) #you won/lost!
        self.texts.append(
            make_surface("Here are your stats:", (400, 150))
            )
        self.texts.append(
            make_surface("Elapsed Time: {} h {} min {} s".format(
                    self.time // 3600000, 
                    self.time // 60000 % 60, 
                    self.time// 1000 % 60,
                    )
                ), (150, 250), to_left=True)
        self.texts.append(
            make_surface("No. of points: {}".format(self.points), (150,300), to_left=True)
        )
