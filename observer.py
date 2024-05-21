class Observer:
    """Class representing an observer in an observer pattern implementation."""

    def __init__(self) -> None:
        """Initialize the Observer object."""
        self.action = 0
        self.infos: list[int] = []

    def alert(self, action: int) -> None:
        """
        Receive an alert from the subject.

        Args:
            action (int): The action to be performed.
        """
        self.action = action

    def act(self, manager) -> None:
        """
        Perform an action based on the alert.

        Args:
            manager: The manager object responsible for handling the action.
        """
        manager.change_state(self.action)
        self.action = 0

    def notify(self, info: int) -> None:
        """
        Receive a notification from the subject.

        Args:
            info (int): The information received from the subject.
        """
        self.infos.append(info)

    def pass_info(self, manager) -> None:
        """
        Pass collected information to the manager.

        Args:
            manager: The manager object responsible for handling the information.
        """
        manager.get_info(self.infos)
