from dataclasses import field

from story.playobject import PlayObject, Narration, Environment, Dialogue, Choice
from story.character import Character
from story.utils import dialogue_task


class Scene:
    # the last choice made by the user
    last_choice = ""

    # history scene index list
    history_scene_indices = []

    # story clip
    story_clip = ""

    # sequence of PlayObjects, including Narration, Dialogue, Environment, Choice
    sequence: list[PlayObject] = field(default_factory=list)

    # current playing index
    current_playing_index = 0

    def play(self):
        if self.current_playing_index >= len(self.sequence):
            return

        play_object = self.sequence[self.current_playing_index]
        play_object.display()
        self.current_playing_index += 1

    def __init__(self, last_choice: str, history_scene_index_list: list[int],
                 story_clip: str, sequence: list[PlayObject] = None, character: Character = None,
                 choice: Choice = None):

        self.last_choice = last_choice
        self.history_scene_indices = history_scene_index_list
        self.story_clip = story_clip

        if sequence is not None:
            self.sequence = sequence
        else:
            self.sequence = []

        print('generating dialogue...')
        # TODO: use simpler format for dialogue generation, such as using \n as delimiter
        response_str = dialogue_task(story_clip, character)

        # keep the text between the first '[Scene]' and the last '[End Scene]' using find() and rfind()
        response_str = response_str[response_str.find("[Scene]"):response_str.rfind("[End Scene]")]

        # remove all the '[Scene]' and '[End Scene]' using replace()
        response_str = response_str.replace("[Scene]", "").replace("[End Scene]", "")

        # split the response string into a list of strings using * as the delimiter
        response_list = response_str.split("*")[1:]

        # construct the sequence of PlayObjects
        for response in response_list:
            # if the response is empty, skip it
            if response == "":
                continue

            # if the response contains no ':', treat it as a Narration
            if ':' not in response:
                self.sequence.append(Narration(response))
                continue

            # split the response using the first ':' as the delimiter
            obj_name, obj_content = response.split(":", 1)
            # remove the possible leading and trailing spaces
            obj_name = obj_name.strip()
            if obj_name == "Narrator" or obj_name == "Narration":
                self.sequence.append(Narration(obj_content))
            elif obj_name == "Environment":
                self.sequence.append(Environment(obj_content))
            else:
                self.sequence.append(Dialogue(obj_name, obj_content))

        if choice is not None:
            self.sequence.append(choice)
