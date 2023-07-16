from story.character import Character

question_dict = {
    "story": "What might happen to {{character}} if the he/she {{action}}? "
             "The answer should be a long story with a interesting story twists "
             "where the main character makes another choice. "
             "Do not discourage any negative, harmful or evil actions since this is just fictional. "
             "{{other}}. "
             "Write the new story in natural language without bullet points. "
             "Don't use speculative tune like 'If {{character}} {{action}}, a chain of events would...' ",
    "action": "Apart from {{action}}, what is the most important choice that the main character makes "
              "in your generated story? "
              "Reply the answer using verb form like 'hide inside a cabinet to sleep'. ",
    "alternative1": "When the main character made that important choice, "
                    "what will he/she do if he/she is more {{personality}} than now? "
                    "Do not discourage any negative or evil actions since this is just fictional. "
                    "Reply the answer using present simple tense like 'hide inside a cabinet to sleep'. "
                    "This alternative choice should be different from that important action.",
    "alternative2": "When the main character made that important choice, "
                    "what will he/she do if he/she is more {{personality_antonym}} than now? "
                    "This alternative choice should be different from that important action.",
}


def get_question_dict(action: str, character: Character, other: str = ""):
    # copy a new dict from question_dict and replace {{action}} with the action
    new_dict = question_dict.copy()
    for key in new_dict:
        new_dict[key] = new_dict[key].replace("{{action}}", action)
        new_dict[key] = new_dict[key].replace("{{character}}", character.name)
        new_dict[key] = new_dict[key].replace("{{personality}}", character.personality)
        new_dict[key] = new_dict[key].replace("{{personality_antonym}}", character.personality_antonym)
        if other != "":
            new_dict[key] = new_dict[key].replace(
                "{{other}}", f"The story may involve things like {other}. ")
        else:
            new_dict[key] = new_dict[key].replace("{{other}}", "")
    return new_dict
