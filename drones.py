class Drone:
    def __init__(self, name: str, path: list[str]) -> None:
        self.name: str = name
        self.path: list[str] = path
        self.in_link: bool = False
        self.index: int = 0

    def on_the_link(self) -> bool:
        return self.in_link

    def is_on_the_goal(self) -> bool:
        if self.index < len(self.path) - 1:
            return False
        return True

    def get_current_zone(self) -> str:
        return self.path[self.index]

    def get_next_zone(self) -> str:
        return self.path[self.index + 1]

    def move(self) -> None:
        self.index += 1
