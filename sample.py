
def get_ram_usage():
    # region imports for ram usage
    import os
    #  endregion imports for ram usage



    pass


def speech_recognition_app():

    # region imports for speech recognition app
    import subprocess

    import speech_recognition
    from speech_recognition import Recognizer
    from speech_recognition import Microphone

    #  endregion imports for speech recognition app

    stopped = False

    script = '~/mp3juicr.sh'

    while not stopped:
        try:
            r = Recognizer()
            with Microphone() as source:
                subprocess.run('clear', shell=True)
                print('Speak now, or forever hold your peace!')
                print("I'm now, listening...")
                print(text := r.recognize_google(r.listen(source)))
                if text == 'run':
                    try:
                        message = f'# [ Executed Using Speech Command "{text}" ]'
                        subprocess.run(f"echo '{message}' >> {script} && bash {script}", shell=True)
                        stopped = True
                    except Exception as useless:
                        print(useless)
                        pass
        except speech_recognition.UnknownValueError as error:
            print('\nencountered an error', error)


    return 200


if __name__ == '__main__':
    exit(speech_recognition_app())
