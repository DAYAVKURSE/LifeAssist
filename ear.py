import speech_recognition
sr = speech_recognition. Recognizer() 
sr.pause_threshold = 0.5


def get_query(botname):
    with speech_recognition.Microphone() as mic:
        sr.adjust_for_ambient_noise (source=mic, duration=0.5)
        while True:
            try:
                print('Computer: Слушаю   ', end="\r")
                audio = sr.listen(source=mic)
                print('Computer: Распознаю', end="\r")
                query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
                if botname:
                    if botname in query:
                        query = query.replace(f'{botname} ', '')
                        break
            except Exception:
                pass
    return query