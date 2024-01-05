import requests


def recuperationDonnees(url: str) -> dict:
    reponse = requests.get(url)
    return reponse.json()

def filter_and_sort_pokemon(varName):
    try:
        results = recuperationDonnees("https://api-pokemon-fr.vercel.app/api/v1/pokemon")

        # Filtre
        filtered_pokemon = [{'name': pokemon['name']['fr'], 'url': pokemon['sprites']['regular']} for pokemon in results if pokemon['name']['fr'].lower().startswith(varName.lower())]

        sorted_pokemon = sorted(filtered_pokemon, key=lambda x: x['name'])

        return sorted_pokemon

    except KeyError:
        print("La réponse JSON ne contient pas la clé 'results'")
        return []

def listeId(idList):
    results = recuperationDonnees("https://api-pokemon-fr.vercel.app/api/v1/pokemon")

    # Filtre
    filtered_pokemon = [{'pokedexId': pokemon['pokedexId'],'name': pokemon['name']['fr'], 'url': pokemon['sprites']['regular']} for pokemon in results if
                        pokemon['pokedexId'] in idList]

    return filtered_pokemon

def getDict(url: str) -> dict:
    data = recuperationDonnees(url)
    dico = {}

    dico['pokedexId'] = getIdPokemon(data)
    dico['nomFR'] = getNomFrPokemon(data)
    dico['nomEN'] = getNomEnPokemon(data)
    dico['types'] = getTypePokemon(data)
    dico['sprite'] = getImageSpritePokemon(data)
    dico['stats'] = getStatPokemon(data)
    dico['pre'] = evolutionsPre(data)
    dico['next'] = evolutionsNext(data)
    dico['resistances'] = getResistances(data)

    return dico

def evolutionsPre(data: dict):
    if(data['evolution']):
        pre = data['evolution']['pre']

        if pre is None:
            return None
        else:
            liste = []
            for i in pre:
                dico = {}
                pre1 = recuperationDonnees(getURLFromName(str(i['pokedexId'])))
                dico['pokedexId'] = pre1['pokedexId']
                dico['nameFR'] = getNomFrPokemon(pre1)
                dico['nameEN'] = getNomEnPokemon(pre1)
                dico['sprite'] = getImageSpritePokemon(pre1)
                dico['types'] = getTypePokemon(pre1)
                dico['condition'] = i['condition']
                liste.append(dico)
            return liste
    return None

def evolutionsNext(data: dict):
    if(data['evolution']):
        next = data['evolution']['next']

        if next is None:
            return None
        else:
            liste = []
            for i in next:
                dico = {}
                next1 = recuperationDonnees(getURLFromName(str(i['pokedexId'])))
                dico['pokedexId'] = next1['pokedexId']
                dico['nameFR'] = getNomFrPokemon(next1)
                dico['nameEN'] = getNomEnPokemon(next1)
                dico['sprite'] = getImageSpritePokemon(next1)
                dico['types'] = getTypePokemon(next1)
                dico['condition'] = i['condition']
                liste.append(dico)
            return liste
    return None


def testDonnees(url: str) -> bool:
    data = recuperationDonnees(url)
    return len(data) != 2

def getIdPokemon(data) -> str:
    return data['pokedexId']

def getNomFrPokemon(data) -> str:
    return data['name']['fr']


def getNomEnPokemon(data) -> str:
    return data['name']['en']


def getTypePokemon(data) -> list:
    types = []
    if data['types'] is not None:
        for typePokemon in range(len(data['types'])):
            types.append(data['types'][typePokemon]['image'])
    return types


def getImageSpritePokemon(data) -> str:
    return data['sprites']['regular']


def getStatPokemon(data) -> dict:
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

def getResistances(data) -> dict:
    return data['resistances']

def getURLFromName(name: str) -> str:
    return "https://api-pokemon-fr.vercel.app/api/v1/pokemon/" + name
