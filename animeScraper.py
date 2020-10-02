from urllib.request import urlopen as uReq

from bs4 import BeautifulSoup as soup
import json
import time

start = time.perf_counter()

class Anime:
    def __init__(self, name, synonyms, type):
        self.name = name
        self.synonyms = synonyms
        self.type = type


scrapedList = []

# scrapedList.append(Anime("Kanojo Okarishimasu", ["Rent a Girlfriend", "Rental Girlfriend"], "Anime").__dict__) # Creates an anime



with open('Assets/AniListAnime.html', 'r') as f:
    contents = f.read()

anime_soup = soup(contents, "html.parser")
anime = anime_soup.findAll("div", {"class":"media-card"})
        
for ani in anime:

    # Get Title
    animeTitle = ani.find("a",{"class":"title"})
    anime_name = animeTitle.text.strip()

    # Get Type

    hoverData = ani.find("div", {"class":"hover-data"})

    infoData = hoverData.find("div", {"class":"info"})

    info_text = infoData.text.strip()

    print(info_text)

    scrapedList.append(Anime(anime_name, [], info_text).__dict__)

json.dump(scrapedList, open("anime.json", "w"), indent=4) # Dumps the list of dictionary versions of the Anime objects to anime.json

print(scrapedList)





finish = time.perf_counter()

print(f"Exited in {round((finish - start), 2)} seconds")
