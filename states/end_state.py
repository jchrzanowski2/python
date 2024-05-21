import pygame
from .game_state import GameState
from constants import Constants, Statistics
from util import make_surface
import json


pygame.font.init()
font = pygame.font.Font(None, 36)


class EndState(GameState):
    def __init__(self, win: bool, time_played: int, statistics: Statistics) -> None:
        super().__init__()
        self.won = "won" if win else "lost"
        self.time = time_played
        self.texts: list[tuple[pygame.Surface, pygame.Rect]] = []
        self.statistics = statistics
        points_for_winning = 2000 if self.won == "won" else 0
        self.statistics.total_points = self.statistics.distance_travelled//10 + self.statistics.points - self.statistics.time//100 + self.statistics.bullets_shot * 10 + points_for_winning
        high_score = load_high_score()
        self.better_score = 0
        if self.statistics.total_points > high_score:
            self.better_score = 1
            save_high_score(self.statistics.total_points)

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
        self.texts.append(
            make_surface(
                "Total points: {}".format(self.statistics.total_points),
                (150, 500),
                to_left=True
            )
        )
        beaten = "beaten" if self.better_score else "not beaten"
        self.texts.append(
            make_surface(
                "You have {} the high score".format(beaten) + ("!" * self.better_score * 3),
                (400, 550)
            )
        )

def save_high_score(score: int) -> None:
    with open(Constants.high_score_file, 'w') as file:
        json.dump({'high_score': score}, file)

def load_high_score():
    try:
        with open(Constants.high_score_file, 'r') as file:
            data = json.load(file)
            return data.get('high_score', 0)
    except FileNotFoundError:
        return 0
