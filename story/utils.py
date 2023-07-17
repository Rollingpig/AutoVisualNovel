from llm.chat import get_response_from_llm
from story.character import Character
from story.prompts import first_run, create_scene


def first_run_qa(story_text: str) -> dict:
    prompt = prompt_from_story_and_qa_dict(story_text, first_run.question_dict)

    answer_dict = {}
    repetition_count = 0
    while answer_dict == {} and repetition_count < 5:
        response_str = get_response_from_llm(prompt, llm_model="gpt-4")
        answer_dict = parse_answer(response_str)
        repetition_count += 1

    prompt_split_2 = prompt_story_split(story_text, answer_dict['action2'])
    response_str_2 = get_response_from_llm(prompt_split_2, llm_model="gpt-4")
    answer_dict['clip1'] = response_str_2

    prompt_split_3 = prompt_story_split(story_text, answer_dict['action3'])
    response_str_3 = get_response_from_llm(prompt_split_3, llm_model="gpt-3.5-turbo")
    answer_dict['clip2'] = response_str_3

    return answer_dict


def later_run_qa(history_stories: str, choice: str, character: Character, element: str) -> dict:
    prompt = prompt_from_story_and_qa_dict(
        history_stories, create_scene.get_question_dict(choice, character, element))

    answer_dict = {}
    repetition_count = 0
    while answer_dict == {} and repetition_count < 5:
        response_str = get_response_from_llm(prompt, llm_model="gpt-4")
        answer_dict = parse_answer(response_str)
        repetition_count += 1

    try:
        prompt_split = prompt_story_split(answer_dict['story'], answer_dict['action'])
        response_str = get_response_from_llm(prompt_split, llm_model="gpt-3.5-turbo")
        answer_dict['clip'] = response_str
    except KeyError:
        print(answer_dict)
        raise KeyError

    return answer_dict


def parse_answer(response_str: str) -> dict:
    # try converting the understanding to a dictionary
    try:
        response_dict = eval(response_str)
    except Exception as e:
        try:
            response_dict = eval(response_str[response_str.find('{'):response_str.rfind('}') + 1])
        except Exception as e:
            print(response_str)
            print("The response_str cannot be converted to a dictionary!")
            return {}

    # iterate through the 'QA' list
    # construct a new dictionary where the key is the 'key' and the value is the 'answer'
    answer_dict = {}
    for qa in response_dict['QA']:
        key = qa['key']
        answer = qa['answer']
        answer_dict[key] = answer
    return answer_dict


def prompt_from_story_and_qa_dict(story: str, question_dictionary: dict) -> str:
    json_str = "{'QA': ["
    for key in question_dictionary:
        json_str += '{ "key": "' + key + '", "question": "' + question_dictionary[key] + '", "answer": "", },'
    json_str += "]}"

    prompt = "You are an AI assistant that understands stories. "
    prompt += "Please read the following story: "
    prompt += story
    prompt += "\n Then please answer the questions specified in the JSON object: \n"
    prompt += json_str
    prompt += "\nWrite the answer in the 'answer' field. " \
              "Ensure the response can be parsed by Python json.loads"
    return prompt


def prompt_story_split(story: str, split: str) -> str:
    # read the prompt from file
    with open("story/prompts/story_split.txt", "r") as f:
        prompt = f.read()

    # replace the placeholder with the story
    prompt = prompt.replace("{{story}}", story)
    prompt = prompt.replace("{{splitEvent}}", split)
    return prompt


def prompt_dialogue(story: str, character: Character) -> str:
    # read the prompt from file
    with open("story/prompts/dialogue.txt", "r") as f:
        prompt = f.read()

    # replace the placeholder with the story
    prompt = prompt.replace("{{story}}", story)
    prompt = prompt.replace("{{character}}", character.name)
    prompt = prompt.replace("{{personality}}", character.personality)
    return prompt


def dialogue_task(story: str, character: Character) -> str:
    prompt = prompt_dialogue(story, character)
    response_str = get_response_from_llm(prompt, llm_model="gpt-3.5-turbo")
    return response_str
