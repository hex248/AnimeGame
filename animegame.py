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

# animeList.append(Anime("Kanojo Okarishimasu", ["Rent a Girlfriend", "Rental Girlfriend"], "Anime").__dict__) # Creates an anime
# animeList.append(Anime("Mayoiga", ["The Lost Village", "Mayoiga"], "Anime").__dict__) # Creates an anime



# json.dump(animeList, open("anime.json", "w"), indent=4) # Dumps the list of dictionary versions of the Anime objects to anime.json

with open("anime.json","r") as dumpedJson: # Opens the database file
    JsonData = dumpedJson.read() # Saves the data in the file to "JsonData"

a = json.loads(JsonData)

animeList = []
movieList = []
allList = []
for x in a:
    # print(x, "\n", type(x), "\n")
    print("\n")
    print(x["name"], "is the name")
    print(x["synonyms"][0], "and", x["synonyms"][1], "are what some other people might call it")
    print(x["type"], "is the type")
    if (x["type"] is "Anime"):
        animeList.append(x)
    elif (x["type"] is "Movie"):
        movieList.append(x)
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