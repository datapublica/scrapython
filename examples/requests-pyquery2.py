## nodisplay
import json
## /nodisplay
from pyquery import PyQuery as pq
import requests

url = u"http://fr.wikipedia.org/wiki/Araignée"
resultat = requests.get(url)
document = pq(resultat.text).make_links_absolute(url)

titles = []
# Sélectionner des éléments
for link in ([a.attr.href for a in document("a").items()][:5]):
    document = pq(requests.get(link).content)
    titles.append(document("title").text())

json.dumps(titles, indent=2)
