from pyquery import PyQuery as pq

doc = """
<html><body>
  <ul class='container'>
      <li id='li-1'>premier li</li>
      <li id='li-2'>deuxieme li</li>
  </ul>
</body></html>
"""

# Créer un document à partir d'une chaîne
selecteur = pq(doc)

# Sélectionner des éléments
selecteur("ul.container").text()
selecteur("#li-1").text()
