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

with open("anime.json","r", encoding = "utf-8") as dumpedJson: # Opens the database file
    JsonData = dumpedJson.read() # Saves the data in the file to "JsonData"

a = json.loads(JsonData, encoding = "utf-8")

animeList = []
movieList = []
allList = []
for x in a:
    if (x["type"] == "TV" or x["type"] == "ONA"):
        animeList.append(x)
    elif (x["type"] == "Movie"):
        movieList.append(x)
    if (x["type"] == "TV" or x["type"] == "Movie" or x["type"] == "ONA"):
        allList.append(x)

print(animeList)
    

root = tk.Tk()
root.title("Anime Game")
root.resizable(False, False)
root.overrideredirect(True)
root.geometry("800x800+560+140")

# frame = tk.Frame(root, bg = "grey", width = 800, height = 800)
# frame.pack(fill = "x")


canvas = tk.Canvas(root, width = 800, height = 800)

canvasBackground = tk.PhotoImage(file = "./Assets/bg.png") # Gets the background image for the canvas
canvasBackgroundLabel = tk.Label(canvas, image = canvasBackground)
canvasBackgroundLabel.place(relwidth = 1, relheight = 1, relx = 0.5, anchor = "n", rely = 0)

animeButtonImage = tk.PhotoImage(file = "./Assets/AnimeButton.png") # Gets the image for the anime button
animeButton = tk.Button(root, image = animeButtonImage, borderwidth=0, relief = "flat", command = lambda: ButtonClick(animeButton), highlightthickness = 0, bd = 0) # Creates the button
animeButton.place(relx = 0.2, rely = 0.5, anchor = "center") # Places the button

movieButtonImage = tk.PhotoImage(file = "./Assets/MovieButton.png") # Gets the image for the movie button
movieButton = tk.Button(root, image = movieButtonImage, borderwidth=0, relief = "flat", command = lambda: ButtonClick(movieButton), highlightthickness = 0, bd = 0) # Creates the button
movieButton.place(relx = 0.5, rely = 0.5, anchor = "center") # Places the button

closeButtonImage = tk.PhotoImage(file = "./Assets/CloseButton1.png") # Gets the image for the close button
closeButton = tk.Button(root, image = closeButtonImage, borderwidth=0, relief = "flat", command = lambda: ButtonClick(closeButton), highlightthickness = 0, bd = 0)
closeButton.place(relx = 0.9, rely = 0.1, anchor = "center")

canvas.pack()


homeButtons = [animeButton, movieButton]

# userEntry = tk.Entry(canvas, font = ("Arial", "30"))
# userEntry.place(relx = 0.5, rely = 0.94, relwidth = 0.95, anchor = "center")

def ButtonClick(button):

    button.place_forget()

    if (homeButtons.__contains__(button)):
        
        for button in homeButtons:

            button.place_forget()
    
    if (button == closeButton):

        root.destroy()


finish = time.perf_counter() # Ends the counter started in line 10

print(f"Exited in {round(finish-start, 2)} seconds(s)") # Prints the time taken to run



root.mainloop()