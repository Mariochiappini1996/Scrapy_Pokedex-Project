import os
import requests

# Mappa generazione → regione
GENERATION_REGION = {
    'generation-i': 'Kanto',
    'generation-ii': 'Johto',
    'generation-iii': 'Hoenn',
    'generation-iv': 'Sinnoh',
    'generation-v': 'Unova',
    'generation-vi': 'Kalos',
    'generation-vii': 'Alola',
    'generation-viii': 'Galar',
    'generation-ix': 'Paldea',
}

BASE_API = 'https://pokeapi.co/api/v2/'

def get_total_pokemon():
    url = BASE_API + 'pokemon?limit=1'
    response = requests.get(url).json()
    return response['count']

def get_pokemon_species_data(species_url):
    response = requests.get(species_url)
    if response.status_code == 200:
        return response.json()
    return None

def download_sprite(pokemon_id, region):
    url = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png'
    response = requests.get(url)
    if response.status_code == 200:
        folder = os.path.join('sprites_pokemon', region)
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, f'{pokemon_id}.png')
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f'Scaricato sprite id={pokemon_id} in {region}/')
    else:
        print(f'Impossibile scaricare sprite id={pokemon_id}')

def main():
    total = get_total_pokemon()
    print(f'Totale Pokémon da scaricare: {total}')

    for poke_id in range(1, total + 1):
        # Ottieni dati specie per la generazione / regione
        species_url = f'{BASE_API}pokemon-species/{poke_id}/'
        species_data = get_pokemon_species_data(species_url)
        if species_data:
            gen_name = species_data['generation']['name']
            region = GENERATION_REGION.get(gen_name, 'Sconosciuta')
            download_sprite(poke_id, region)
        else:
            print(f'Impossibile recuperare specie id={poke_id}')

if __name__ == '__main__':
    main()
