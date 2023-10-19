import requests

def recuperationDonnees(url : str) -> dict:
    reponse = requests.get(url)
    return reponse.json()


def getNomFrPokemon(url : str) -> str:
    data = recuperationDonnees(url)
    return data['name']['fr']

def getNomEnPokemon(url : str) -> str:
    data = recuperationDonnees(url)
    return data['name']['en']

def getTypePokemon(url : str) -> list:
    data = recuperationDonnees(url)
    types = []
    for typePokemon in range(len(data['types'])):
        types.append(data['types'][typePokemon]['name'])
    return types

def getImageSpritePokemon(url : str) -> str:
    data = recuperationDonnees(url)
    return data['sprites']['regular']

def getStatPokemon(url : str) -> dict:
    data = recuperationDonnees(url)
    return data['stats']