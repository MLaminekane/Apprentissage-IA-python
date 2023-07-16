import openai
import os
from tkinter import *

class OpenAIAssistantGUI:
    def __init__(self, api_key):
        self.root = Tk()
        self.root.title("MLK")

        os.environ['OPENAI_Key'] = api_key
        openai.api_key = os.environ['OPENAI_Key']

        self.engine = 'text-davinci-003'
        self.max_tokens = 512

        self.txt = Text(self.root, font=("times new roman", 15))
        self.txt.grid(row=0, column=0, columnspan=4)

        self.e = Entry(self.root, width=100)
        self.e.grid(row=1, column=0)
        self.e.bind("<Return>", self.envoie)

        self.envoyer = Button(self.root, text="Send", command=self.envoie)
        self.envoyer.grid(row=1, column=1)

    def set_engine(self, engine):
        self.engine = engine

    def set_max_tokens(self, max_tokens):
        self.max_tokens = max_tokens

    def generate_response(self, prompt):
        response = openai.Completion.create(engine=self.engine, prompt=prompt, max_tokens=self.max_tokens)
        return response.choices[0].text

    def envoie(self, event=None):
        prompt = self.e.get()
        reponse_text = self.generate_response(prompt)
        envoie = "User: " + prompt + "\n" + "MLK: " + reponse_text
        self.txt.insert(END, envoie + "\n")
        self.e.delete(0, END)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    API_KEY = ''
    assistant = OpenAIAssistantGUI(api_key=API_KEY)
    assistant.run()
