import ear
import chat_gpt
import mouth

#import subprocess
import traceback


# command_list = [{'func':'run notepad.exe','world_speech_calls':{'EN-en':['open notebook','run notes'],'RU-ru':['запусти блокнот','открой блокнот']}, 'exec':'''import os\nos.system('notepad.exe')'''}]
bot_name = 'компьютер'
command_list = []
computer_feature_list = []
current_state = {}
user_feature_list = {'lang':'RU-ru'}


def load_command_list():
    global command_list
    with open('command_list.txt', "r", encoding='utf-8') as f:
        command_list = f.readlines()

def add_command():
    global command_list
    with open('command_list.txt', "w", encoding='utf-8') as f:
        f.writelines(command_list)


def check_an_command_in_list(query):
    global command_list
    for command in command_list:
        command = eval(command)
        if query in command['world_speech_calls'][user_feature_list['lang']]:
            return True
    else:
        return False

def add_call_in_list(query,lang,analog_call):
    global command_list
    for command in command_list:
        command = eval(command)
        if analog_call in command['world_speech_calls'][lang]:
            if user_feature_list['lang'] in command['world_speech_calls'].keys():
                if query not in command['world_speech_calls'][user_feature_list['lang']]:
                    command['world_speech_calls'][user_feature_list['lang']].append(query)
                else:
                    print('Такая команда уже существует')
                    return False
            else:
                command['world_speech_calls'].update({user_feature_list['lang']: [query]})

        if query in command['world_speech_calls'][lang]:
            return True
    else:
        print('Нет аналогичной команды')
        return False
    
if __name__ == '__main__':
    load_command_list()
    chat_gpt.auth(chat_gpt.global_api_key)

    while True:
        query = ear.get_query(bot_name) #input('Пишите: ') #ear.get_query()
        print('User: ',query)
        if check_an_command_in_list(query):
            for command in command_list:
                command = eval(command)
                if query in command['world_speech_calls'][user_feature_list['lang']]:
                    try:
                        print('Выполняю код: ',command['exec'].replace("'''","'"))
                        responce = exec(command['exec'].replace("'''","'"))
                    except Exception as e:
                        responce = f'Команда выполнена c исключением: {str(e)[:100]}'
                        print(traceback.format_exc())
                    if not responce:
                        responce = 'Команда выполнена'

        if query == 'создай новую команду':
            func = input('Computer: Введите имя команды, которое максимально точно будет соответствовать тому, что она делает: ')
            if func in command_list:
                print('Computer: Такая команда уже существует')
                continue
            else:
                bot_responce = chat_gpt.need_help(func)
                print('Bot_helper: ',bot_responce)
                query = input('Computer: Введите Enter, если команда подходит, или введите в ответ свою: ')
                if query == '':
                    if '```python' in bot_responce:
                        bot_responce = bot_responce.split('```python')[1].split('```')[0]
                    command = bot_responce 
                else:
                    command = query
                try:
                    print('Выполняю код: ',command.replace("'''","'"))
                    responce = exec(command.replace("'''","'"))
                except Exception as e:
                    responce = f'Команда выполнена c исключением: {str(e)[:100]}'
                    print(traceback.format_exc())
                if not responce:
                    responce = 'Команда выполнена'
                print('Computer: ',responce)
                mouth.speech(responce)
                if input('Введите s, чтобы сохранить макрос, или любую клавишу, чтобы перезаписать: ') in ['S','s']:
                    command_list.append({'func':func,'world_speech_calls':{user_feature_list['lang']:[query]}, 'exec':f'''{command}'''})
                    add_command()
                    break
                else:
                    continue

        elif query == 'добавь ключевое слово':
            for i, responce in enumerate(['произнесите аналогичную команду','произнесите новую команду']):
                print('Computer: ',responce)
                mouth.speech(responce)
                while True:
                    try:
                        action = ear.get_query(bot_name)
                    except Exception:
                        continue
                    else:
                        if action:
                            break
                if i:
                    analog_call = action
                else:
                    query = action
            lang = user_feature_list['lang']
            analog_call = action
            responce = 'Команда добавлена.' if add_call_in_list(query,lang,analog_call) else 'Не удалось добавить команду'
            add_command()

        else:
                responce = f'Действие не распознано. Скажите "{bot_name}, создай новую команду" или "{bot_name}, добавь ключевое слово".'

                # for _ in range(5):
                #     # action = input('Computer: Введите команду n или аналогичную команду: ')
                #     while True:
                #         try:
                #             action = ear.get_query(bot_name)
                #         except Exception:
                #             continue
                #         else:
                #             if action:
                #                 break

                        # commands[query] = chat_gpt.get_responce(data)
                    # else:
            #         #     raise ValueError('Неверная команда')
            #     else:
            #         raise ValueError('Ошибка добавления данных.')
            # except ValueError as e:
            #     responce = f'Ошибка значения: {str(e)[:100]}'
            # except Exception as e:
            #     responce = f'Неизвестная ошибка: {str(e)[:100]}'

            # commands[query] = chat_gpt.get_responce(query)
        print('Computer: ',responce)
        mouth.speech(responce)