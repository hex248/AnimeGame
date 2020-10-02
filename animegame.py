import tkinter as tk
import string
import Levenshtein
import random

import time

start = time.perf_counter()

animeFile = open("anime.txt", "r")

animelist = []

for anime in animeFile:
    animelist.append(anime)

root = tk.Tk()
root.title("Anime Game")

canvas = tk.Canvas(root, width = 800, height = 800)
canvas.pack()

animeButtonImage = tk.PhotoImage(file = "./Assets/AnimeButton.png")
animeButton = tk.Button(canvas, image = animeButtonImage, borderwidth=0, relief = "sunken", command = lambda: ButtonClick(animeButton))
animeButton.place(relx = 0.25, rely = 0.5, anchor = "center")

movieButtonImage = tk.PhotoImage(file = "./Assets/MovieButton.png")
movieButton = tk.Button(canvas, image = movieButtonImage, borderwidth=0, relief = "sunken", command = lambda: ButtonClick(movieButton))
movieButton.place(relx = 0.5, rely = 0.5, anchor = "center")

hentaiButtonImage = tk.PhotoImage(file = "./Assets/HentaiButton.png")
hentaiButton = tk.Button(canvas, image = hentaiButtonImage, borderwidth=0, relief = "sunken", command = lambda: ButtonClick(hentaiButton))
hentaiButton.place(relx = 0.75, rely = 0.5, anchor = "center")

homeButtons = [animeButton, movieButton, hentaiButton]

# userEntry = tk.Entry(canvas, font = ("Arial", "30"))
# userEntry.place(relx = 0.5, rely = 0.94, relwidth = 0.95, anchor = "center")

def ButtonClick(button):

    button.place_forget()

    if (homeButtons.__contains__(button)):
        
        for button in homeButtons:

            button.place_forget()

finish = time.perf_counter()

print(f"Finished in {round(finish-start, 1)} seconds(s)")



root.mainloop()