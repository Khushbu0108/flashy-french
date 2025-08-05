import random
from sys import orig_argv
from tkinter import *

import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn_french = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data= pandas.read_csv("data/french_words.csv")
    to_learn_french = original_data.to_dict(orient="records")
else:
    to_learn_french = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card= random.choice(to_learn_french)

    canvas.itemconfig(french, text= "French", fill = "black")
    canvas.itemconfig(fr_meaning, text= current_card["French"], fill = "black")


    canvas.itemconfig(front_canvas, image = front_card_photo)
    flip_timer = window.after(3000, func = flip_card)

def flip_card():
    canvas.itemconfig(french, text="English", fill = "white")
    canvas.itemconfig(fr_meaning, text = current_card["English"], fill = "white")
    canvas.itemconfig(front_canvas, image = back_card_photo)


def is_known():
    to_learn_french.remove(current_card)
    print(len(to_learn_french))
    data = pandas.DataFrame(to_learn_french)
    data.to_csv("data/words_to_learn.csv", index=False)

    next_card()

window = Tk()
window.title("Flashy")
window.minsize(width = 850, height=576)
window.config(padx = 50, pady=50, bg= BACKGROUND_COLOR, highlightthickness= 0 )
flip_timer = window.after(3000, flip_card)
#canvas
canvas= Canvas(width =  800, height=526, highlightthickness= 0 )
canvas.grid(row=0, column=0, columnspan=2)
canvas.config(bg = BACKGROUND_COLOR)

#front image
front_card_photo = PhotoImage(file = "images/card_front.png")
front_canvas = canvas.create_image( 400, 263, image = front_card_photo )

back_card_photo = PhotoImage(file = "images/card_back.png")

# labels
french = canvas.create_text(400, 150, text = "French", fill = "black", font = ("arial", 40, "italic"))
fr_meaning = canvas.create_text(400, 263, text = "meaning", fill = "black", font = ("arial", 60, "bold") )


#Buttons
wrong_photo = PhotoImage(file = "images/wrong.png")
wrong_button = Button(image= wrong_photo, padx=50, pady=50, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column = 0)

right_photo = PhotoImage(file = "images/right.png")
right_button = Button(image = right_photo, padx = 50, pady= 50, highlightthickness=0, command=is_known)
right_button.grid(row=1, column =1)

next_card()
# back photo


window.mainloop()

