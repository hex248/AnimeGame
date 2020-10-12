import datetime
import json
import time
import requests
from bs4 import BeautifulSoup as soup

class Anime:
    def __init__(self, japanese, othernames, type, aired, genres):
        self.japanese = japanese
        self.othernames = othernames
        self.type = type
        self.aired = aired
        self.genres = genres

start = time.perf_counter()

scrapedList = []
ignoreList = []

animePage = requests.get("https://gogoanime.so/anime-list-0")

anime_soup = soup(animePage.text, "html.parser") # Gets the soup of the html file
rows = anime_soup.findAll("li", {"class":"first-char"}) # Finds each row (#, A, B, C, D etc.)

rows.remove(rows[0])

previousEntry = "EMPTY STRING"

print(rows)

for row in rows:

    a = row.find("a")

    row_link = "https://gogoanime.so" + a["href"]

    page = requests.get(row_link)

    page_soup = soup(page.text, "html.parser")
    
    pagination = page_soup.find("div", {"class":"anime_name_pagination"})



    pagesHrefs = []

    pages = pagination.findAll("li")
    if (pages):

        for page in pages:
            href = page.find("a")["href"]
            print(href)
            pagesHrefs.append(row_link + href)
            
    else:

        pagesHrefs = [row_link]


    for page in pagesHrefs:
        
        print("Found page", page, "in", pagesHrefs)

        pageNo = requests.get(page)

        page_soup = soup(pageNo.text, "html.parser")

        body = page_soup.find("div", {"class": "anime_list_body"})

        entries = body.findAll("li")

        for entry in entries:

            a = entry.find("a")

            anime_link = "https://gogoanime.so" + a["href"]

            page = requests.get(anime_link)

            page_soup = soup(page.text, "html.parser")



            # Get Japanese name

            japanese_name = page_soup.find("h1").text.strip()

            if ("(Dub)" in japanese_name or "Season" in japanese_name or "Movie" in japanese_name or previousEntry in japanese_name or japanese_name in previousEntry):

                ignoreList.append(japanese_name)

            if (not ignoreList.__contains__(japanese_name)):

                previousEntry = japanese_name
                
                print("\n")
                print(japanese_name)



                # Get Other names

                othernamesSpan = page_soup.find("span", text = "Other name: ")

                othernamesSpanParent = othernamesSpan.parent

                othernames = []

                if (len(othernamesSpanParent.text.strip()) > 12): # If there are any other names (https://gogoanime.so/category/227 is an example of an entry without)

                    othernames = othernamesSpanParent.text.strip().split("Other name: ")[1]

                    othernames = othernames.split(", ")

                print("Other Names:", othernames)



                # Get Type

                typeSpan = page_soup.find("span", text = "Type: ")

                typeSpanParent = typeSpan.parent

                anime_type = typeSpanParent.find("a").text.strip()

                # Make types more uniform (Fall 2020 Anime = TV and TV Series = TV)

                if ("Anime" in anime_type or "TV" in anime_type):
                    anime_type = "TV"
                elif ("OVA" in anime_type):
                    anime_type = "OVA"
                elif ("ONA" in anime_type):
                    anime_type = "ONA"
                elif ("Special" in anime_type):
                    anime_type = "Special"
                elif ("Music" in anime_type):
                    anime_type = "Music"
                elif ("Movie" in anime_type):
                    anime_type = "Movie"

                print("Type:", anime_type)



                # Get Date

                dateSpan = page_soup.find("span", text = "Released: ")

                anime_date = "Unknown"

                if (len(dateSpan.parent.text.strip()) > 10): # If there is a release date (https://gogoanime.so/category/xia-gan-yi-dan-shen-jianxin is an example of an entry without)

                    anime_date = dateSpan.parent.text.strip().split("Released: ")[1]

                print("Date:", anime_date)



                # Get Genres

                genresSpan = page_soup.find("span", text = "Genre: ")

                genresSpanParent = genresSpan.parent

                genres = []

                genresA = genresSpanParent.findAll("a")

                for genre in genresA:

                    genre = genre.text.strip().split(", ")

                    genre = genre[len(genre) - 1]

                    genres.append(genre)

                print("Genres:", genres)

                scrapedList.append(Anime(japanese_name, othernames, anime_type, anime_date, genres).__dict__)



json.dump(scrapedList, open("anime.json", "w", encoding = "utf-8"), indent = 4, ensure_ascii = False) # Dumps the list of dictionary versions of the Anime objects to anime.json

print(scrapedList)

finish = time.perf_counter()

print(f"Exited in {round((finish - start), 2)} seconds")