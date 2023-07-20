import json
import os

import requests
from bs4 import BeautifulSoup

URL = "https://www.leagueoflegends.com/fr-fr/champions/"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')
champs = soup.find_all(
    "a", class_="style__Wrapper-n3ovyt-0 style__ResponsiveWrapper-n3ovyt-4 ehjaZK elVPdk style__Item-sc-13btjky-3 CanXV isVisible isFirstTime")

# Json file
filename = 'components/scraped.json'
listObj = []

if os.path.isfile(filename) is False:
    if not os.path.exists('components'):
        os.mkdir('components')
    print("File not found")
    print("\nGenerating File \"scraped.json\"")
    filename = "components/scraped.json"
    with open(filename, 'w') as json_file:
        pass

print("\nThis may take some time...")

for champ in champs:
    champ = champ.get("href")
    new_url = URL + champ[17:]
    r = requests.get(new_url)

    soup = BeautifulSoup(r.content, 'html5lib')
    imgs = soup.find_all(
        "img", class_="style__NoScriptImg-g183su-0 style__Img-g183su-1 cipsic dBitJH")

    skins = []
    passive = []
    spells = []
    abilities = []
    for img in imgs:
        if "splash" in img.get("src"):
            skins.append(img.get("src"))
        if "ability" in img.get("src"):
            abilities.append(img.get("src"))
        if "spell" in img.get("src"):
            spells.append(img.get("src"))
        if "passive" in img.get("src"):
            passive.append(img.get("src"))
    listObj.append({champ[17:-1]: [skins, passive, spells, abilities]})


with open(filename, 'w') as json_file:
    json.dump(listObj, json_file,
              indent=4,
              separators=(',', ': '))

print("\nFinished Scraping")
