class Observer:
    def __init__(self) -> None:
        self.action = 0

    def notify(self, action: int) -> None:
        self.action = action
    
    def act(self, manager) -> bool:
        manager.change_state(self.action)
        self.action = 0
        return False
