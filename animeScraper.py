from urllib.request import urlopen as uReq

from bs4 import BeautifulSoup as soup
import json
import time
import requests
from lxml import html

class Anime:
    def __init__(self, name, synonyms, type):
        self.name = name
        self.synonyms = synonyms
        self.type = type

start = time.perf_counter()


scrapedList = []
ignoreList = []

with open('Assets/animepaheList.html', 'r', encoding = "utf8") as f:
    contents = f.read()

anime_soup = soup(contents, "html.parser") # Gets the soup of the html file

tabContent = anime_soup.find("div", {"class":"tab-content"}) # Gets the main content of the page
rows = tabContent.findAll("div", {"class":"row"}) # Finds each row (#, A, B, C, D etc.)
for row in rows:

    animelist = row.findAll("a")

    for ani in animelist:


        # Get individual page link

        anime_link = ani["href"]

        print("Link:", anime_link) # Prints the link

        page = requests.get(anime_link) # Requests the html of the link

        page_soup = soup(page.text, "html.parser") # Creates a soup of the new html


        # Get Japanese title

        try:

            japaneseTitle = page_soup.find("h2", {"japanese"}) # Finds the h2 tag with "japanese"

            japanese_name = japaneseTitle.text.strip() # Gets the text for the japanese name

        except:

            japanese_name = "" # If there is no Japanese name, set it to an empty string
            
        print(japanese_name)


        # Get English title

        anime_info = page_soup.find("div", {"class":"anime-info"}) # Gets the info panel

        englishStrong = anime_info.find("strong", text = "English: ") # Gets the strong with the text: "English:"

        try:
            
            english_name = englishStrong.next_sibling # Gets the sibling of the strong

        except:

            english_name = "" # If there is no sibling of the strong, add it to the ignore list

        if (japanese_name == "" and english_name == ""):

            ignoreList.append(japanese_name)

        if (not ignoreList.__contains__(japanese_name)):

            print("Japanese:", japanese_name) # Prints "Japanese: [japanese_name]"

            print("English:", english_name) # Prints "English: [english_name]"

            # Get type

            typeStrong = anime_info.find("strong", text = "Type:") # Finds the "Type:" strong within the info panel

            animeP = typeStrong.find_parent("p").getText() # Gets all of the text displayed in the p tag which is the parent of <strong>Type:</strong>

            anime_type = animeP.replace("Type: ", "") # Removes "Type: " from the string

            print("Type:", anime_type,"\n") # Prints "Type: [type]"


            if (anime_type == "TV" or "MOVIE" or "ONA"): # If it is a show or a movie

                scrapedList.append(Anime(japanese_name, [english_name], anime_type).__dict__) # Creates an anime entry with all of the data that was just collected



json.dump(scrapedList, open("anime.json", "w", encoding = "utf-8"), indent = 4, ensure_ascii = False) # Dumps the list of dictionary versions of the Anime objects to anime.json

print(scrapedList)





finish = time.perf_counter()

print(f"Exited in {round((finish - start), 2)} seconds")
