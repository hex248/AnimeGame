import json
import Levenshtein
from Levenshtein import distance
from stop_words import get_stop_words
import random
import string
import time
import tkinter as tk
from statemachine import StateMachine, State
import romkan

from googletrans import Translator

translator = Translator()

# End of imports

class Anime:
    def __init__(self, japanese, othernames, type, aired, genres):
        self.japanese = japanese
        self.othernames = othernames
        self.type = type
        self.aired = aired
        self.genres = genres

start = time.perf_counter() # Starts a counter to measure the exit time of the script

class GlobalState(StateMachine):
    home = State("Home", initial = True)
    gameAnime = State("Anime")
    gameMovie = State("Movie")
    gameAll = State("All")

    goHome = gameAnime.to(home) | gameMovie.to(home) | gameAll.to(home)
    goAnime = home.to(gameAnime)
    goMovie = home.to(gameMovie)
    goAll = home.to(gameAll)

    def on_goHome(self):
        print("home")
    def on_goAnime(self):
        print("anime")
    def on_goMovie(self):
        print("movie")
    def on_goAll(self):
        print("all")

gameState = GlobalState()

animeList = []

# json.dump(animeList, open("anime.json", "w"), indent=4) # Dumps the list of dictionary versions of the Anime objects to anime.json

with open("anime.json","r", encoding = "utf-8") as dumpedJson: # Opens the database file
    JsonData = dumpedJson.read() # Saves the data in the file to "JsonData"

animeJson = json.loads(JsonData)

animeList = []
movieList = []
allList = []
gameList = []
for x in animeJson:
    if (x["type"] == "TV" or x["type"] == "ONA"):
        animeList.append(x)
    elif (x["type"] == "Movie"):
        movieList.append(x)
    if (x["type"] == "TV" or x["type"] == "Movie" or x["type"] == "ONA"):
        allList.append(x)

# Converting to Romaji -- NOT CURRENTLY WORKING

# fixedList = []

# for x in allList:
#     romaji_name = romkan.to_hepburn(x["name"])
#     english_name = translator.translate(romaji_name, dest="en").text

#     print(f"Romaji: {romaji_name}\nEnglish: {english_name}")

#     type = x["type"]

#     aired = x["aired"]

#     fixedList.append(Anime(romaji_name, english_name, type, aired).__dict__)



root = tk.Tk()
root.title("Anime Game")
root.resizable(False, False)
#root.overrideredirect(True)
root.geometry("800x800+560+140")

root.bind("<Return>", lambda event: sendButtonClick(gameState.current_state))

# frame = tk.Frame(root, bg = "grey", width = 800, height = 800)
# frame.pack(fill = "x")

# Home Screen Elements

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

allButtonImage = tk.PhotoImage(file = "./Assets/AllButton.png") # Gets the image for the movie button
allButton = tk.Button(root, image = allButtonImage, borderwidth=0, relief = "flat", command = lambda: ButtonClick(allButton), highlightthickness = 0, bd = 0) # Creates the button
allButton.place(relx = 0.8, rely = 0.5, anchor = "center") # Places the button


# Utility Elements

closeButtonImage = tk.PhotoImage(file = "./Assets/CloseButton1.png") # Gets the image for the close button
closeButton = tk.Button(root, image = closeButtonImage, borderwidth=0, relief = "flat", command = lambda: ButtonClick(closeButton), highlightthickness = 0, bd = 0)
closeButton.place(relx = 0.9875, rely = 0.0125, anchor = "ne")

backButtonImage = tk.PhotoImage(file = "./Assets/BackButton.png")
backButton = tk.Button(root, image = backButtonImage, borderwidth=0, relief = "flat", command = lambda: ButtonClick(backButton), highlightthickness = 0, bd = 0)

# Game Elements

sendButtonImage = tk.PhotoImage(file = "./Assets/SendButton.png") # Gets the image for the send/submit button
sendButton = tk.Button(root, image = sendButtonImage, borderwidth = 0, relief = "flat", command = lambda: sendButtonClick(gameState.current_state), highlightthickness = 0, bd = 0)

userEntryImage = tk.PhotoImage(file = "./Assets/SendButton.png")
userEntry = tk.Entry(root, borderwidth = 0, relief = "flat", highlightthickness = 0, bd = 0, font = ("Arial", 30))

canvas.pack()


homeButtons = [animeButton, movieButton, allButton]
pageElements = [sendButton, backButton, userEntry]

def ButtonClick(button):

    button.place_forget()

    if (button == animeButton):

        gameState.goAnime()

    elif (button == movieButton):

        gameState.goMovie()

    elif (button == allButton):

        gameState.goAll()

    elif (button == backButton):

        gameState.goHome()

        animeButton.place(relx = 0.2, rely = 0.5, anchor = "center") # Places the button
        movieButton.place(relx = 0.5, rely = 0.5, anchor = "center") # Places the button
        allButton.place(relx = 0.8, rely = 0.5, anchor = "center") # Places the button

        for element in pageElements:

            element.place_forget()

    if (homeButtons.__contains__(button)):
        
        for button in homeButtons:

            button.place_forget()

        for element in pageElements:

            placeInPos(element)
    
    if (button == closeButton):

        root.destroy()

def sendButtonClick(state):

    if (state == gameState.gameAnime or state == gameState.gameMovie or state == gameState.gameAll):

        # Anime specific stuff

        checkInput(gameList, userEntry.get())

    

def checkInput(list, input = userEntry.get()):

    input = input.lower()

    punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    for char in input:
        if (char in punctuation):
            input.replace(char, "")

    if (not input.strip() or input.strip() == "" or input.strip() in punctuation):
        return

    if (gameState.current_state is gameState.gameAnime):
        list = animeList.copy()
    elif (gameState.current_state is gameState.gameMovie):
        list = movieList.copy()
    elif (gameState.current_state is gameState.gameAll):
        list = allList.copy()

    possibleChoices = []
    
    for x in list:
        name = x["japanese"].lower().replace("movie", "")
        
        stopwords = get_stop_words("en")
        
        if (input not in stopwords):# if the name contains the input then remove that part of it. if what remains is less than 15 chars long, or the levenshtein distance from the input and the full name is less than 2, then move on.
            if ((input in name and len(name.replace(input, "").strip()) < 15) or distance(input, name) < 2):
                possibleChoices.append(x)
        
        for othername in x["othernames"]:

            othername = othername.lower().replace("movie", "").strip()
            othername = othername.lower().replace("tv", "").strip()
            othername = othername.lower().replace("ona", "").strip()

            othername = othername.lower()

            if (input not in stopwords):
                if (((input in othername and len(othername.replace(input, "").strip()) < 15) or distance(input, othername) < 2) and not possibleChoices.__contains__(x)):
                    possibleChoices.append(x)

    if (possibleChoices != []):
        for choice in possibleChoices:
            print(choice["japanese"])
    else:
        print("none found")



def placeInPos(element):

    if (element == backButton):

        element.place(relx = 0.0125, rely = 0.0125, anchor = "nw")
    
    elif (element == sendButton):

        element.place(relx = 0.5, rely = 0.9875, anchor = "s")

    elif (element == userEntry):

        element.place(relx = 0.5, rely = 0.8, relwidth = 0.4, relheight = 0.1, anchor = "s")


finish = time.perf_counter() # Ends the counter started in line 10

print(f"Exited in {round(finish-start, 2)} second(s)") # Prints the time taken to run



root.mainloop()