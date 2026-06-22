class Drone:
    def __init__(self, id: int, name: str, path: list[str]) -> None:
        self.name: str = name
        self.path: list[str] = path
        self.in_link: bool = False
        self.current_index: int = 0
        self.id = id

    def on_the_link(self) -> bool:
        return self.in_link

    def is_on_the_goal(self) -> bool:
        if self.current_index < len(self.path) - 1:
            return False
        return True

    def get_current_zone(self) -> str:
        return self.path[self.current_index]

    def get_next_zone(self) -> str:
        return self.path[self.current_index + 1]

    def move(self) -> None:
        self.current_index += 1
