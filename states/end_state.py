import pygame
from .game_state import GameState
from constants import Constants, Statistics
from util import make_surface

pygame.font.init()
font = pygame.font.Font(None, 36)


class EndState(GameState):
    def __init__(self, win: bool, time_played: int, statistics: Statistics) -> None:
        super().__init__()
        self.won = "won" if win else "lost"
        self.time = time_played
        self.texts: list[tuple[pygame.Surface, pygame.Rect]] = []
        self.statistics = statistics
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
        )  # you won/lost!
        self.texts.append(make_surface("Here are your stats:", (400, 150)))
        self.texts.append(
            make_surface(
                "Elapsed Time: {} h {} min {} s".format(
                    self.time // 3600000,
                    self.time // 60000 % 60,
                    self.time // 1000 % 60,
                ),
                (150, 250),
                to_left=True,
            )
        )
        self.texts.append(
            make_surface(
                "No. of points: {}".format(self.statistics.points),
                (150, 300),
                to_left=True,
            )
        )
        self.texts.append(
            make_surface(
                "Distance travelled: {}m".format(
                    int(self.statistics.distance_travelled / 10) / 5
                ),
                (150, 350),
                to_left=True,
            )
        )
        self.texts.append(
            make_surface(
                "Bullets shot: {}".format(self.statistics.bullets_shot),
                (150, 400),
                to_left=True,
            )
        )
        self.texts.append(
            make_surface(
                "Kills: {}".format(self.statistics.kills), (150, 450), to_left=True
            )
        )
