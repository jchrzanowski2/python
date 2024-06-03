import pygame
from pygame.event import Event
from .game_state import GameState
from constants import Constants
from util import make_surface
import json


class ScoreState(GameState):
    def __init__(self) -> None:
        super().__init__()
        try:
            with open(Constants.high_score_file, "r") as file:
                self.scores = json.load(file)
        except FileNotFoundError:
            self.scores = {
                "name": ["", "", "", "", "", "", "", "", "", ""],
                "score": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            }
        self.texts: list[tuple[pygame.Surface, pygame.Rect]] = []
        self.add_texts()

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(Constants.LIGHT_GREEN)
        for surface, rect in self.texts:
            screen.blit(surface, rect)

    def update(self) -> None:
        pass

    def handle_events(self, event: Event) -> None:
        pass

    def add_texts(self):
        y_offset = 100
        self.texts.append(make_surface("Top Scores", (400, y_offset)))
        y_offset += 40
        for name, score in zip(self.scores["name"], self.scores["score"]):
            if name == "":
                name = "''"
            self.texts.append(make_surface(f"{name}: {score}", (400, y_offset)))
            y_offset += 30
