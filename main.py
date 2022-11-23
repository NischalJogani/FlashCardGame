import pandas
from random import *
from tkinter import *


# -------------------- CONSTANTS ------------------ #
BACKGROUND_COLOR = "#B1DDC6"
rand_card = {}
need_to_learn = {}

try:
    words = pandas.read_csv("data/words_to_learn.csv.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    need_to_learn = original_data.to_dict(orient="records")
else:
    need_to_learn = words.to_dict(orient="records")


def next_card():
    global rand_card, flip_timer
    window.after_cancel(flip_timer)
    rand_card = choice(need_to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=rand_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front)
    flip_timer = window.after(4000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=rand_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back)


def is_known():
    need_to_learn.remove(rand_card)
    print(len(need_to_learn))
    words_df = pandas.DataFrame(need_to_learn)
    words_df.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# -------------------- UI Setup ------------------- #
window = Tk()
window.title("Flash Card Game")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(4000, func=flip_card)

# Card, Right and Wrong image
canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="French", font=("Ariel", 35, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 40, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)


# Buttons:
cross_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=cross_image, command=next_card)
wrong_button.config(bg=BACKGROUND_COLOR, highlightthickness=0)
wrong_button.grid(row=1, column=0)

tick_image = PhotoImage(file="images/right.png")
right_button = Button(image=tick_image, command=is_known)
right_button.config(bg=BACKGROUND_COLOR, highlightthickness=0)
right_button.grid(row=1, column=1)


next_card()


window.mainloop()
