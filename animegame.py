import json
import Levenshtein
import random
import string
import time
import tkinter as tk

# End of imports

start = time.perf_counter() # Starts a counter to measure the exit time of the script

class Anime:
    def __init__(self, name, synonyms, type):
        self.name = name
        self.synonyms = synonyms
        self.type = type

animeList = []


# json.dump(animeList, open("anime.json", "w"), indent=4) # Dumps the list of dictionary versions of the Anime objects to anime.json

with open("anime.json","r") as dumpedJson: # Opens the database file
    JsonData = dumpedJson.read() # Saves the data in the file to "JsonData"

a = json.loads(JsonData)

animeList = []
movieList = []
allList = []
for x in a:
    if (x["type"] is "TV"):
        animeList.append(x)
    elif (x["type"] is "Movie"):
        movieList.append(x)
    if (x["type"] == "TV" or x["type"] == "Movie"):
        allList.append(x)
    

root = tk.Tk()
root.title("Anime Game")

canvas = tk.Canvas(root, width = 800, height = 800)
canvas.pack()

animeButtonImage = tk.PhotoImage(file = "./Assets/AnimeButton.png") # Gets the image for the anime button
animeButton = tk.Button(canvas, image = animeButtonImage, borderwidth=0, relief = "sunken", command = lambda: ButtonClick(animeButton)) # Creates the button
animeButton.place(relx = 0.2, rely = 0.5, anchor = "center") # Places the button

movieButtonImage = tk.PhotoImage(file = "./Assets/MovieButton.png") # Gets the image for the movie button
movieButton = tk.Button(canvas, image = movieButtonImage, borderwidth=0, relief = "sunken", command = lambda: ButtonClick(movieButton)) # Creates the button
movieButton.place(relx = 0.5, rely = 0.5, anchor = "center") # Places the button

homeButtons = [animeButton, movieButton]

# userEntry = tk.Entry(canvas, font = ("Arial", "30"))
# userEntry.place(relx = 0.5, rely = 0.94, relwidth = 0.95, anchor = "center")

def ButtonClick(button):

    button.place_forget()

    if (homeButtons.__contains__(button)):
        
        for button in homeButtons:

            button.place_forget()

finish = time.perf_counter() # Ends the counter started in line 10

print(f"Exited in {round(finish-start, 2)} seconds(s)") # Prints the time taken to run



root.mainloop()