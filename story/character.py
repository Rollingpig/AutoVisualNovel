from dataclasses import field

from story.playobject import PlayObject


class Character(PlayObject):
    name: str = ""
    description: str = ""  # two sentences, generated by LLM
    personality: str = ""  # one word, generated by LLM
    personality_antonym: str = ""  # one word, generated by LLM
    personality_score = 2.0  # changed along the game play
    personality_dict: dict[int, str] = {}  # generated by LLM. key: personality_score, value: personality_description

    def __init__(self, dictionary: dict = None):
        if dictionary is not None:
            self.parse(dictionary)

    def display(self):
        print(f'The main character is {self.name}. {self.description}. {self.get_current_personality()}')
        # print(f'the personality is {self.personality}')
        # print(f'the personality score is {self.personality_score}')

    def get_current_personality(self) -> str:
        """
        Get the current personality description based on the current personality score.
        :return: current personality description
        """
        if self.personality_dict == {}:
            return ""

        # round the personality score to integer
        rounded_score = round(self.personality_score)
        # clip the score to [1, 5]
        rounded_score = max(1, min(5, rounded_score))
        # get the current personality description
        current_personality_description = self.personality_dict[rounded_score]

        return current_personality_description

    def parse(self, dictionary: dict):
        self.name = dictionary["character_name"]
        self.description = dictionary["character_description"]
        self.personality = dictionary["character_personality"]
        self.personality_antonym = dictionary["personality_antonym"]
        if "personality_spectrum_1" in dictionary:
            self.personality_dict = {
                1: dictionary["personality_spectrum_1"],
                2: dictionary["personality_spectrum_2"],
                3: dictionary["personality_spectrum_3"],
                4: dictionary["personality_spectrum_4"],
                5: dictionary["personality_spectrum_5"]
            }
