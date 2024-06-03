import pygame
from .game_state import GameState
from .button import Button
from pygame.event import Event
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
        self.buttons: list[Button] = []
        self.buttons.append(
            Button(
                "Show scoreboard",
                320,
                570,
                lambda: self.observer.alert(Constants.Actions.GAME_SCORE),
                color=Constants.BROWN,
            )
        )
        self.statistics = statistics
        points_for_winning = 2000 if self.won == "won" else 0
        self.statistics.total_points = int(
            int(self.statistics.distance_travelled / 5) / 5
            + self.statistics.points
            - self.statistics.time // 100
            + self.statistics.bullets_shot * 10
            + points_for_winning
        )
        high_scores = load_high_scores()
        self.better_score = 0
        if self.statistics.total_points > high_scores["score"][-1]:
            self.better_score = 1
            my_score = self.statistics.total_points
            my_name = Constants.nickname
            current_score = high_scores["score"][0]
            index = 1
            while my_score < current_score:
                current_score = high_scores["score"][index]
                index += 1
            index -= 1

            tmp_scores = [i for i in high_scores["score"]]
            tmp_names = [i for i in high_scores["name"]]

            high_scores["name"][index] = my_name
            high_scores["score"][index] = my_score
            index += 1

            for i in range(index, len(high_scores["score"])):
                high_scores["name"][i] = tmp_names[i - 1]
                high_scores["score"][i] = tmp_scores[i - 1]

            save_high_scores(high_scores)

        self.add_texts()

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(Constants.LIGHT_GREEN)
        for surface, rect in self.texts:
            screen.blit(surface, rect)
        for button in self.buttons:
            button.draw(screen)

    def update(self) -> None:
        return super().update()

    def handle_events(self, event: Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.clicked(x, y):
                    button.function()

    def add_texts(self):
        self.texts.append(
            make_surface("You {}!".format(self.won), (400, 70))
        )  # you won/lost!
        self.texts.append(make_surface("Here are your stats:", (400, 120)))
        self.texts.append(
            make_surface(
                "Elapsed Time: {} h {} min {} s".format(
                    self.time // 3600000,
                    self.time // 60000 % 60,
                    self.time // 1000 % 60,
                ),
                (150, 220),
                to_left=True,
            )
        )
        self.texts.append(
            make_surface(
                "No. of points: {}".format(self.statistics.points),
                (150, 270),
                to_left=True,
            )
        )
        self.texts.append(
            make_surface(
                "Distance travelled: {}m".format(
                    int(self.statistics.distance_travelled / 10) / 5
                ),
                (150, 320),
                to_left=True,
            )
        )
        self.texts.append(
            make_surface(
                "Bullets shot: {}".format(self.statistics.bullets_shot),
                (150, 370),
                to_left=True,
            )
        )
        self.texts.append(
            make_surface(
                "Kills: {}".format(self.statistics.kills), (150, 420), to_left=True
            )
        )
        self.texts.append(
            make_surface(
                "Total points: {}".format(self.statistics.total_points),
                (150, 470),
                to_left=True,
            )
        )
        beaten = "got" if self.better_score else "not got"
        self.texts.append(
            make_surface(
                "You have {} in top 10".format(beaten) + ("!" * self.better_score * 3),
                (400, 520),
            )
        )


def save_high_scores(scores: list) -> None:
    with open(Constants.high_score_file, "w") as file:
        json.dump(scores, file)


def load_high_scores() -> list:
    try:
        with open(Constants.high_score_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "name": ["", "", "", "", "", "", "", "", "", ""],
            "score": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        }
