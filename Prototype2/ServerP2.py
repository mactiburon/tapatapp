import Prototype2.dadesServer as dades
from Prototype2.dadesServer import User

# Exemple d'ús de la llista d'usuaris
for x in dades.users:
    print(x)

# Exemple d'ús de la classe User
a= User(id=1, username="Kurl", password="12345", email="prova2@gmail.com")
print(a)
