import requests

url = "http://fr.wikipedia.org/wiki/Araignée"
resultat = requests.get(url)

resultat.status_code
resultat.text[:104]
