from pygame.event import Event
from .game_state import GameState
from .input import InputBox
from constants import Constants
from .button import Button
from util import make_surface
import pygame


class MenuState(GameState):
    def __init__(self) -> None:
        super().__init__()
        self.buttons: list[Button] = []
        self.buttons.append(
            Button(
                "Start game",
                320,
                400,
                lambda: self.observer.alert(Constants.Actions.GAME_START),
                color=Constants.BROWN,
            )
        )
        self.box = InputBox(303, 300, 140, 32)
        self.texts: list[tuple[pygame.Surface, pygame.Rect]] = []
        self.add_texts()

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(Constants.LIGHT_GREEN)
        for button in self.buttons:
            button.draw(screen)
        self.box.draw(screen)
        for surface, rect in self.texts:
            screen.blit(surface, rect)

    def update(self) -> None:
        self.box.update()

    def handle_events(self, event: Event) -> None:
        self.box.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.clicked(x, y):
                    button.function()

    def add_texts(self):
        self.texts.append(make_surface("Welcome to Shooter!", (400, 100)))
        self.texts.append(make_surface("Type nickname and press enter:", (400, 270)))
