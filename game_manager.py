from constants import Constants
from states import *
import pygame

class GameManager:
    def __init__(self) -> None:
        self.current_state: GameState = RunState()
    
    def handle_events(self, event: pygame.event.Event) -> None:
        self.current_state.handle_events(event)

    def draw(self, screen: pygame.Surface) -> None:
        self.current_state.draw(screen)
    
    def update(self) -> None:
        self.current_state.update()
    
    def change_state(self, action: int) -> None:
        if action == Constants.Actions.GAME_END:
            self.current_state = EndState(
                self.current_state.world.stop, 
                pygame.time.get_ticks() - self.current_state.start_time,
                self.current_state.player.points
                )


