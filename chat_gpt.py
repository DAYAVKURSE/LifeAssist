import openai
from openai.error import AuthenticationError
# указываем ключ из личного кабинета openai

global_api_key = "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"
def auth(api_key):
    global global_api_key
    if api_key == "":
        api_key = global_api_key
    else:
        # global global_api_key
        global_api_key = api_key
    openai.api_key = api_key

def get_responce(messages, query):
    if "Выйди из чата" in query: 
        return None

    messages.append({"role": "user", "content": query})
    for _ in range(3):
        try:
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = messages)
        except AuthenticationError:
            print("Неверный ключ авторизации")
            auth(input('Введите ключ авторизации(или нажмите Enter, если используется актуальный): '))
            continue
        break
    reply = chat.choices[0].message.content
    messages.append({"role":"assistant", "content": reply})
    return reply

def need_help(data):
    query = f'''
    Я бот на ОС Windows и языке python 3.11. 
    Пользователь ввел такую команду: {data}. 
    Напиши в одном окне, с импортом необходимых модулей, если нужно, код, который выполнит команду пользователя при помощи exec() python.
    '''
    return get_responce(query)