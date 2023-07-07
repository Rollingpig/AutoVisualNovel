import openai

from llm.base import ChatSequence, Message


def chat_with_gpt(chat_sequence: ChatSequence) -> (str, ChatSequence):
    response = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model="gpt-4",
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
            model="gpt-3.5-turbo",
            messages=chat_sequence.raw()
        )
        content = response['choices'][0]['message']['content']
        finish_reason = response['choices'][0]['finish_reason']
        result += content

    if finish_reason == 'stop':
        return result, chat_sequence
    else:
        raise Exception(f"Unexpected finish reason: {finish_reason}")