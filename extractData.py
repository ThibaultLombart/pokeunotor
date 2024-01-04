import requests


def recuperationDonnees(url: str) -> dict:
    reponse = requests.get(url)
    return reponse.json()


def getDict(url: str) -> dict:
    dico = {}

    dico['nomFR'] = getNomFrPokemon(url)
    dico['nomEN'] = getNomEnPokemon(url)
    dico['types'] = getTypePokemon(url)
    dico['sprite'] = getImageSpritePokemon(url)
    dico['stats'] = getStatPokemon(url)

    return dico



def testDonnees(url: str) -> bool:
    data = recuperationDonnees(url)
    return len(data) != 2

def getIdPokemon(url : str) -> str:
    data = recuperationDonnees(url)
    return data['pokedexId']

def getNomFrPokemon(url: str) -> str:
    data = recuperationDonnees(url)
    return data['name']['fr']


def getNomEnPokemon(url: str) -> str:
    data = recuperationDonnees(url)
    return data['name']['en']


def getTypePokemon(url: str) -> list:
    data = recuperationDonnees(url)
    types = []
    if data['types'] is not None:
        for typePokemon in range(len(data['types'])):
            types.append(data['types'][typePokemon]['image'])
    return types


def getImageSpritePokemon(url: str) -> str:
    data = recuperationDonnees(url)
    return data['sprites']['regular']


def getStatPokemon(url: str) -> dict:
    data = recuperationDonnees(url)
    stats = data['stats']
    if stats is None:
        stats = {}
        stats['hp'] = 0
        stats['atk'] = 0
        stats['def'] = 0
        stats['spe_atk'] = 0
        stats['spe_def'] = 0
        stats['vit'] = 0
    return stats


def getURLFromName(name: str) -> str:
    return "https://api-pokemon-fr.vercel.app/api/v1/pokemon/" + name
