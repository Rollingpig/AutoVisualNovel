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
    pass


class Dialogue(PlayObject):
    pass


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


class Scene:
    # TODO: construct dialogue and environment from story clip, conditioned on character personalities
    # TODO: also try using GPT-3.5 instead of GPT-4

    # the last choice made by the user
    last_choice = ""

    # history scene index list
    history_scene_indices = []

    # story clip
    story_clip = ""

    # sequence of PlayObjects, including Narration, Dialogue, Environment, Choice
    sequence: list[PlayObject] = field(default_factory=list)

    def __init__(self, last_choice: str = "", history_scene_index_list: list[int] = None,
                 story_clip: str = "", sequence: list[PlayObject] = None):
        if last_choice != "":
            self.last_choice = last_choice
        if history_scene_index_list is not None:
            self.history_scene_indices = history_scene_index_list
        if story_clip != "":
            self.story_clip = story_clip
        if sequence is not None:
            self.sequence = sequence
        else:
            self.sequence = []
