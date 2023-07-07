from dataclasses import field

import story.utils
from story.character import Character
from story.playobject import Narration, Choice, Scene


class Story:
    original_text = ""  # store the original story text
    summary = ""  # summary of the original story text, generated by LLM
    element = ""  # element of the original story text, generated by LLM

    character: Character = None

    scenes: list[Scene] = field(default_factory=list)
    current_scene_index = 0

    def __init__(self, story_text: str = ""):
        if story_text != "":
            self.original_text = story_text

        # initialize the scenes list
        self.scenes = []

    def play(self):
        print("-" * 30)

        # display the character if it is the first scene
        if self.current_scene_index == 0:
            self.character.display()

        # display current scene
        scene = self.scenes[self.current_scene_index]
        for play_object in scene.sequence:
            play_object.display()

    def init_understand(self):
        """
        Initialize the story by understanding the story text.
        Generally, this function will identify the character, character description, and choices in the story.
        And construct initial scenes using choices.
        """
        # Get the answer dictionary from the first run QA
        answer_dict = story.utils.first_run_qa(self.original_text)

        # get basic info of the story
        self.summary = answer_dict['summary']
        self.element = answer_dict['element']

        # construct the character by parsing the answer dictionary
        self.character = Character(answer_dict)

        # construct scenes
        self.construct_first_run_scene(answer_dict)

    def construct_first_run_scene(self, answer_dict: dict):
        story_text = self.original_text

        # skip constructing the first scene
        # construct the second scene
        index2 = story.utils.non_precise_locate(story_text, answer_dict['division2'])
        choice2 = Choice([answer_dict['action2'], answer_dict['alternative3'], answer_dict['alternative4']])
        new_scene = Scene(
            last_choice=answer_dict['action1'],
            history_scene_index_list=[self.current_scene_index],
            story_clip=story_text[:index2],
            sequence=[Narration(story_text[:index2]), choice2]
        )
        self.scenes.append(new_scene)

        # construct the third scene
        index3 = story.utils.non_precise_locate(story_text, answer_dict['division3'])
        choice3 = Choice([answer_dict['action3'], answer_dict['alternative5'], answer_dict['alternative6']])
        new_scene2 = Scene(
            last_choice=answer_dict['action2'],
            history_scene_index_list=[self.current_scene_index, self.scenes.index(new_scene)],
            story_clip=story_text[index2:index3],
            sequence=[Narration(story_text[index2:index3]), choice3]
        )
        self.scenes.append(new_scene2)

    def generate_scene_from_choice(self, choice_index: int):
        """
        Generate a new scene from the choice made by the user
        """
        current_scene = self.scenes[self.current_scene_index]
        last_play_object = current_scene.sequence[-1]
        if not isinstance(last_play_object, Choice):
            raise ValueError("Last play object is not a Choice object!")
        else:
            current_choices: Choice = last_play_object
            choice = current_choices.content[choice_index - 1]

            # iterate through the scenes list to find the scene with the last choice
            for scene in self.scenes:
                if scene.last_choice == choice:
                    self.current_scene_index = self.scenes.index(scene)
                    return None

            # if the scene with the last choice is not found, generate a new scene
            print("Generating new story...")

            # get history stories by combining the latest 10 history scene summaries from the history scene index list
            history_stories = ""
            for index in current_scene.history_scene_indices[-min(10, len(current_scene.history_scene_indices)):]:
                history_stories += self.scenes[index].story_clip + " "
            # add current scene story clip to history stories
            history_stories += current_scene.story_clip

            # prompt for story generation
            # TODO: summarize the earliest 10 history scenes
            # TODO: reflect the character personality from history and update it
            answer_dict = story.utils.later_run_qa(
                history_stories, choice, self.character, self.element)

            # configure the new scene
            story_text = answer_dict['story']
            division_index = story.utils.non_precise_locate(story_text, answer_dict['division'])
            history_indices = current_scene.history_scene_indices.copy()
            history_indices.append(self.current_scene_index)
            new_scene = Scene(
                last_choice=choice,
                history_scene_index_list=history_indices,
                story_clip=story_text[:division_index] + " " + answer_dict['division'],
                sequence=[Narration(story_text[:division_index] + " " + answer_dict['division']),
                          Choice([answer_dict['action'], answer_dict['alternative1'], answer_dict['alternative2']])],
            )
            self.scenes.append(new_scene)
            self.current_scene_index = self.scenes.index(new_scene)
