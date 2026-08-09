from services.pokemon_data_downloader import PokemonDataDownloader

downloader = PokemonDataDownloader()

result = downloader.download_cards()

print("WYNIK:", result)
