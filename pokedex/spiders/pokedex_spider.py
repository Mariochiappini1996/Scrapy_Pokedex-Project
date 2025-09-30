import scrapy

# Mappatura regione e anno per generazione (base esemplificativa)
GENERATION_INFO = {
    'generation-i': {'anno': 1996, 'regione': 'Kanto'},
    'generation-ii': {'anno': 1999, 'regione': 'Johto'},
    'generation-iii': {'anno': 2002, 'regione': 'Hoenn'},
    'generation-iv': {'anno': 2006, 'regione': 'Sinnoh'},
    'generation-v': {'anno': 2010, 'regione': 'Unova'},
    'generation-vi': {'anno': 2013, 'regione': 'Kalos'},
    'generation-vii': {'anno': 2016, 'regione': 'Alola'},
    'generation-viii': {'anno': 2019, 'regione': 'Galar'},
    'generation-ix': {'anno': 2022, 'regione': 'Paldea'},
}

class PokedexCompleteSpider(scrapy.Spider):
    name = "pokedex_complete"
    allowed_domains = ["pokeapi.co"]
    start_urls = ["https://pokeapi.co/api/v2/pokemon?limit=1200&offset=0"]  # limiti alti per coprire tutto

    def parse(self, response):
        data = response.json()
        for poke in data['results']:
            yield scrapy.Request(poke['url'], callback=self.parse_pokemon)
        # Paginazione
        next_page = data.get('next')
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_pokemon(self, response):
        p = response.json()
        # Chiedi anche dati specie per generazione (anno e regione)
        species_url = p['species']['url']
        meta = {
            'pokemon_data': p
        }
        yield scrapy.Request(species_url, callback=self.parse_species, cb_kwargs=meta)

    def parse_species(self, response, pokemon_data):
        species = response.json()
        gen_name = species['generation']['name']  # es. generation-i
        gen_info = GENERATION_INFO.get(gen_name, {'anno': None, 'regione': None})

        yield {
            'id': pokemon_data['id'],
            'name': pokemon_data['name'],
            'types': [t['type']['name'] for t in pokemon_data['types']],
            'abilities': [a['ability']['name'] for a in pokemon_data['abilities']],
            'height': pokemon_data['height'],
            'weight': pokemon_data['weight'],
            'sprite_url': pokemon_data['sprites']['front_default'],
            'generation': gen_name,
            'region': gen_info['regione'],
            'year': gen_info['anno'],
            'image_urls': [pokemon_data['sprites']['front_default']] if pokemon_data['sprites']['front_default'] else []
        }
