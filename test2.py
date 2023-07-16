import tkinter as tk
import speech_recognition as sr
import pyttsx3
import openai

openai.api_key = ''

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

conversation = ""
user_name = "MLK"
bot_name = "MLK_Ai"

def generate_response(prompt):
    global conversation
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=conversation + prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    response_str = response["choices"][0]["text"].replace("\n", "")
    response_str = response_str.split(user_name + ":", 1)[0].split(bot_name + ":", 1)[0]

    conversation += user_name + ":" + prompt + "\n" + bot_name + ":" + response_str + "\n"
    return response_str

def start_listening():
    global conversation
    global mic
    global r

    with mic as source:
        print("\n POSEZ VOTRE QUESTION...")
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    print("no longer listening")

    try:
        user_input = r.recognize_google(audio)
    except:
        return

    response_str = generate_response(user_input)
    print(response_str)

    engine.say(response_str)
    engine.runAndWait()

def send_question():
    global conversation
    global question_entry
    global engine

    user_input = question_entry.get()
    response_str = generate_response(user_input)
    print(response_str)

    engine.say(response_str)
    engine.runAndWait()

    conversation += user_name + ":" + user_input + "\n" + bot_name + ":" + response_str + "\n"
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, user_name + ":" + user_input + "\n")
    chat_text.insert(tk.END, bot_name + ":" + response_str + "\n")
    chat_text.config(state=tk.DISABLED)
    question_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Assistant vocal")

question_label = tk.Label(root, text="Question :")
question_label.pack()

question_entry = tk.Entry(root, width=50)
question_entry.pack()

listen_button = tk.Button(root, text="Ecouter", command=start_listening)
listen_button.pack()

send_button = tk.Button(root, text="Envoyer", command=send_question)
send_button.pack()

chat_label = tk.Label(root, text="Conversation :")
chat_label.pack()

chat_text = tk.Text(root, width=50, height=20)
chat_text.pack()
chat_text.config(state=tk.DISABLED)

root.mainloop()
