import os
import openai
import google.generativeai as palm
from typing import Literal

from llm.base import ChatSequence, Message

MODEL = Literal["gpt-4", "gpt-3.5-turbo", "text-davinci-003", "palm"]


def chat_with_gpt(chat_sequence: ChatSequence, llm_model: MODEL = "gpt-4") -> (str, ChatSequence):
    response = openai.ChatCompletion.create(
        model=llm_model,
        messages=chat_sequence.raw()
    )

    content = response['choices'][0]['message']['content']
    finish_reason = response['choices'][0]['finish_reason']
    result = content

    # if the finish reason is 'length', then the response is truncated
    # we need to let the model know that it can continue
    while finish_reason == 'length':
        chat_sequence.append(Message("assistant", content))
        chat_sequence.append(Message("user", "please continue"))
        response = openai.ChatCompletion.create(
            model=llm_model,
            messages=chat_sequence.raw()
        )
        content = response['choices'][0]['message']['content']
        finish_reason = response['choices'][0]['finish_reason']
        result += content

    if finish_reason == 'stop':
        return result, chat_sequence
    else:
        raise Exception(f"Unexpected finish reason: {finish_reason}")


def chat_with_palm(chat_sequence: ChatSequence) -> (str, ChatSequence):
    # PaLM cannot handle message history.
    response = palm.chat(messages=chat_sequence[0].content + chat_sequence[1].content)

    return response.last, chat_sequence


def get_response_from_llm(prompt: str, llm_model: MODEL = 'gpt-4') -> str:
    # print(prompt)

    chat_seq = ChatSequence()
    chat_seq.append(Message(role="system",
                            content="You are an AI assistant that understands stories."))
    chat_seq.append(Message(role="user", content=prompt))

    if llm_model == 'palm':
        result_str, chat_seq = chat_with_palm(chat_seq)
    else:
        result_str, chat_seq = chat_with_gpt(chat_seq, llm_model=llm_model)

    # if there is no directory named 'debug', create one
    if not os.path.exists("debug"):
        os.makedirs("debug")

    # save result_str to file, if there exists a file with the same name, append the result_str to the file
    with open("debug/result_log.txt", "a") as f:
        f.write(result_str + "\n")

    return result_str
