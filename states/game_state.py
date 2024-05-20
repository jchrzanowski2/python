import pygame
from observer import Observer


class GameState:
    def __init__(self) -> None:
        self.observer = None

    def handle_events(self, event: pygame.event.Event) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pass

    def attach(self, observer: Observer) -> None:
        self.observer = observer
