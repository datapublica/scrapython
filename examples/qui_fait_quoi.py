# -*- coding: utf-8 -*-
## nodisplay
import csv
from pyquery import PyQuery as pq
import json
import requests
## /nodisplay
# Lit les données
people = csv.reader(open("scrapy/people.csv"))
next(people)  # Passer l'en-tête

data = []
for full_name, in people:
    # Coupe (arbitrairement) le prenom au premier espace
    prenom, nom = full_name.split(" ", 1)
    url = "http://fr.linkedin.com/pub/dir/?first=%s&last=%s" % (prenom, nom)

    resultat = requests.get(url)
    document = pq(resultat.text).make_links_absolute(url)

    link = document("#result-set h2 strong a").attr.href
    ## nodisplay
    # Améliore l'extraction en ne prenant que quelqu'un bossant en France
    vcards = document("#result-set li.vcard")
    for vcard in vcards.items():
        if "france" in vcard(".location").text().lower():
            link = vcard("h2 strong a").attr.href
            break
    ## /nodisplay
    boulot, image = None, None
    if link:
        profil = requests.get(link)
        document = pq(profil.text).make_links_absolute(link)
        boulot = [p.text().strip() for p in document(".current li").items()]
        image = document("#profile-picture img").attr.src

    data.append({"name": full_name, "boulot": boulot,
                 "image": image, "url": link})
## nodisplay
json.dump(data, open("qui_fait_quoi.json", "w"), indent=2)
## /nodisplay
