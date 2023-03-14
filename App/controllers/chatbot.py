import openai
import os

a1 = "sk-BGnlSu6qwg"
a2 = "SFD1CHiTc9T3Blbk"
a3 = "FJScqmD4tX1lmeo0hG9IAh"
openai.api_key = a1+a2+a3

def start_conversation():
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="User: Hello\nAI:",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text

def get_ai_response(conversation_history, user_input):
    prompt = f"User: {user_input}\nAI: {conversation_history}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text

def call_until_return_response(func, history, input):
    result = func(history,input)
    while not result:
        result = func(history,input)
    return result