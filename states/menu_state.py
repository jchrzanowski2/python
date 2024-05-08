from pygame.event import Event
from .game_state import GameState
from constants import Constants
from util import Button, make_surface
import pygame

class MenuState(GameState):
    def __init__(self) -> None:
        super().__init__()
        self.buttons: list[Button] = []
        self.buttons.append(Button("Start game", 150, 400, lambda: self.observer.alert(Constants.Actions.GAME_START)))
        self.texts: list[tuple[pygame.Surface, pygame.Rect]] = []
        self.add_texts()

    def draw(self, screen: pygame.Surface) -> None:
        for button in self.buttons:
            button.draw(screen)
        for surface, rect in self.texts:
            screen.blit(surface, rect)
    
    def update(self) -> None:
        pass
    
    def handle_events(self, event: Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.clicked(x,y):
                    button.function()

    def add_texts(self):
        self.texts.append(
            make_surface("Welcome to Shooter!", (400, 100))
            )
        

    
