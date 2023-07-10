import os

from llm.base import ChatSequence, Message
from llm.chat import chat_with_gpt
from story.character import Character
from story.prompts import first_run, create_scene


def first_run_qa(story_text: str) -> dict:
    prompt = prompt_from_story_and_qa_dict(story_text, first_run.question_dict)
    response_str = get_response_from_llm(prompt)
    answer_dict = parse_answer(response_str)

    prompt_split_2 = prompt_story_split(story_text, answer_dict['action2'])
    response_str_2 = get_response_from_llm(prompt_split_2, llm_model="gpt-3.5-turbo")
    answer_dict['clip1'] = response_str_2

    prompt_split_3 = prompt_story_split(story_text, answer_dict['action3'])
    response_str_3 = get_response_from_llm(prompt_split_3, llm_model="gpt-3.5-turbo")
    answer_dict['clip2'] = response_str_3

    # prompt_personality = prompt_persona(
    #     answer_dict['character_name'], answer_dict['character_personality'], answer_dict['personality_antonym'])
    # response_str_personality = get_response_from_llm(prompt_personality, llm_model="gpt-3.5-turbo")
    # answer_dict['personality_spectrum_1'] = response_str_personality.split("---")[0]
    # answer_dict['personality_spectrum_2'] = response_str_personality.split("---")[1]
    # answer_dict['personality_spectrum_3'] = response_str_personality.split("---")[2]
    # answer_dict['personality_spectrum_4'] = response_str_personality.split("---")[3]
    # answer_dict['personality_spectrum_5'] = response_str_personality.split("---")[4]

    return answer_dict


def later_run_qa(history_stories: str, choice: str, character: Character, element: str) -> dict:
    prompt = prompt_from_story_and_qa_dict(
        history_stories, create_scene.get_question_dict(choice, character, element))
    response_str = get_response_from_llm(prompt)
    answer_dict = parse_answer(response_str)
    return answer_dict


def parse_answer(response_str: str) -> dict:
    # try converting the understanding to a dictionary
    try:
        response_dict = eval(response_str)
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


def prompt_persona(character_name: str, persona1: str, persona2: str) -> str:
    # read the prompt from file
    with open("story/prompts/personality.txt", "r") as f:
        prompt = f.read()

    # replace the placeholder with the story
    prompt = prompt.replace("{{character}}", character_name)
    prompt = prompt.replace("{{persona1}}", persona1)
    prompt = prompt.replace("{{persona2}}", persona2)
    return prompt


def get_response_from_llm(prompt: str, llm_model='gpt-4') -> str:
    # print(prompt)

    chat_seq = ChatSequence()
    chat_seq.append(Message(role="system",
                            content="You are an AI assistant that understands stories."))
    chat_seq.append(Message(role="user", content=prompt))
    result_str, chat_seq = chat_with_gpt(chat_seq, llm_model=llm_model)

    # if there is no directory named 'debug', create one
    if not os.path.exists("debug"):
        os.makedirs("debug")

    # save result_str to file, if there exists a file with the same name, append the result_str to the file
    with open("debug/result_log.txt", "a") as f:
        f.write(result_str + "\n")

    return result_str


def remove_punctuation(text: str) -> str:
    text = text.replace('.', ' ')
    text = text.replace(',', ' ')
    text = text.replace('?', ' ')
    text = text.replace('!', ' ')
    text = text.replace(';', ' ')
    text = text.replace(':', ' ')
    text = text.replace('\'', ' ')
    text = text.replace('\"', ' ')
    text = text.replace('(', ' ')
    text = text.replace(')', ' ')
    text = text.replace('-', ' ')
    text = text.replace('_', ' ')
    return text


def non_precise_locate(text: str, query_str: str):
    """
    choose first words of query_str, and find its location in text
    # TODO: find a better way to locate query_str in text
    """
    query_str_list = query_str.split()
    query_str_list = query_str_list[:min(10, len(query_str_list))]
    query_str = ' '.join(query_str_list)

    # locate the query_str in text, ignore case and punctuation
    new_text = text.lower()
    query_str = query_str.lower()
    new_text = remove_punctuation(new_text)
    query_str = remove_punctuation(query_str)

    index = new_text.find(query_str)
    if index == -1:
        raise ValueError("Cannot find query_str in text!")
    return index
