import json

file = "database/pokemon_cards.json"


with open(file, "r", encoding="utf-8") as f:

    cards = json.load(f)


print("LICZBA KART:", len(cards))


card = cards[0]


print("\nPIERWSZA KARTA:")

print("NAZWA:", card.get("name"))

print("NUMER:", card.get("number"))

print("SET:", card.get("set"))

print("RARITY:", card.get("rarity"))

print("OBRAZ:", card.get("images", {}).get("large"))
