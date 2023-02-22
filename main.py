import tkinter
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
words_to_learn = {}


try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    words_to_learn = original_data.to_dict(orient="records")
else:
    words_to_learn = data.to_dict(orient="records")


def choose_new_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(words_to_learn)
    current_f_word = current_card["French"]
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_f_word, fill="black")
    canvas.itemconfig(canvas_img, image=card_front)
    flip_timer = window.after(3000, func=flip)


def is_known():
    words_to_learn.remove(current_card)
    df = pandas.DataFrame(words_to_learn)
    df.to_csv("data/words_to_learn.csv", index=False)
    choose_new_word()


def flip():
    current_e_word = current_card["English"]
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_e_word, fill="white")
    canvas.itemconfig(canvas_img, image=card_back)


# window

window = tkinter.Tk()
window.title("Flashy")
window.config(padx=50, pady=35, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip)


canvas = tkinter.Canvas(width=800, height=526)
card_front = tkinter.PhotoImage(file="images/card_front.png")
card_back = tkinter.PhotoImage(file="images/card_back.png")
canvas_img = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)


x_image = tkinter.PhotoImage(file="images/wrong.png")
x_button = tkinter.Button(image=x_image, highlightthickness=0, command=choose_new_word)
x_button.grid(column=0, row=1)

y_image = tkinter.PhotoImage(file="images/right.png")
y_button = tkinter.Button(image=y_image, highlightthickness=0, command=is_known)
y_button.grid(column=1, row=1)

choose_new_word()

window.mainloop()
