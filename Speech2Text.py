import speech_recognition as sr

class Speecher():
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.speech = ""

    def listenTo(self):
        with sr.Microphone() as source:
            print("Say something!")
            audio = self.recognizer.listen(source)
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            self.speech = self.recognizer.recognize_google(audio)
            print("Google Speech Recognition thinks you said " + self.speech)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        print("Returned " + self.speech)
        return self.speech


spchr = Speecher()
spchr.listenTo()

