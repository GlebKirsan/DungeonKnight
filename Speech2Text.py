import speech_recognition as sr


class Speecher:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.speech = ""

    def listen_to(self):
        with sr.Microphone() as source:
            print("Say something!")
            audio = self.recognizer.listen(source)
        try:
            self.speech = self.recognizer.recognize_google(audio)
            print("Google Speech Recognition thinks you said " + self.speech)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        print("Returned " + self.speech)
        return self.speech
