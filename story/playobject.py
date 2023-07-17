from dataclasses import dataclass, field


@dataclass
class PlayObject:
    raw = ""

    def display(self):
        print(self.raw)


class Narration(PlayObject):
    def __init__(self, raw: str = ""):
        self.raw = raw

    def display(self):
        print(self.raw)


class Environment(PlayObject):
    def __init__(self, raw: str = ""):
        self.raw = raw

    def display(self):
        print(f"[Environment]: {self.raw}")


class Dialogue(PlayObject):
    character: str = ""
    content: str = ""

    def __init__(self, character: str = "", content: str = ""):
        self.character = character
        self.content = content

    def display(self):
        print(f"[{self.character}]: {self.content}")


class Choice(PlayObject):
    content: list[str] = field(default_factory=list)

    def __init__(self, content: list[str] = None):
        if content is not None:
            self.content = content

    def display(self):
        # if content is empty or None, raise error
        if len(self.content) == 0:
            raise ValueError("Choice content is empty!")
        print("-" * 20)
        print("What shall the character do? : ")
        for i in range(len(self.content)):
            print(f"{i + 1}. {self.content[i]}")
