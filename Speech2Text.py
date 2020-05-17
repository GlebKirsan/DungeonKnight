import speech_recognition as sr


class Speecher:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = False
        self.speech = ""

    def listen_to(self):
        with sr.Microphone() as source:
            print("Say something!")
            audio = self.recognizer.listen(source)
        try:
            self.speech = self.recognizer.recognize_google(audio)
            print(f"Google Speech Recognition thinks you said {self.speech}")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

        print(f"Returned {self.speech}")
        return self.speech


    def listen(self, dict):
        with sr.Microphone() as source:
            print("Say something!")
            audio = self.recognizer.listen(source)
        try:
            dict["command"] = self.recognizer.recognize_google(audio)
            self.speech = dict["command"]
            print(f"Google Speech Recognition thinks you said {self.speech}")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")


    def loop_listen_to(self, dict):
        with sr.Microphone() as source:
            while True:
                print("Say something:")
                audio = self.recognizer.listen(source)
                try:
                    dict["command"] = self.recognizer.recognize_google(audio)
                    command = dict["command"]
                    print(f"Google Speech Recognition thinks you said {command}")
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                # return (self.recognizer.recognize_google(audio))
