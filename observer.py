class Observer:
    def __init__(self) -> None:
        self.action = 0
        self.infos: list[int] = []

    def alert(self, action: int) -> None:
        self.action = action
    
    def act(self, manager) -> None:
        manager.change_state(self.action)
        self.action = 0
    
    def notify(self, info: int) -> None:
        self.infos.append(info)
    
    def pass_info(self, manager) -> None:
        manager.get_info(self.infos)

