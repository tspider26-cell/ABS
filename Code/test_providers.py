from services.providers.pokemon_api_provider import PokemonAPIProvider
from services.providers.web_card_provider import WebCardProvider


card = {
    "family": "Pokemon",
    "name": "Spritzee",
    "set": "Perfect Order",
    "code": "POR",
    "number": "035/088",
    "rarity": "Common"
}


print("=" * 40)
print("ABS PROVIDERS TEST v1.0")
print("=" * 40)

print()

pokemon = PokemonAPIProvider()
print(pokemon.search(card))

print()

web = WebCardProvider()
print(web.search(card))

print()

print("=" * 40)
