from services.card_search_service import CardSearchService


card = {

    "family": "Pokemon",
    "set": "WL035",
    "number": "035/088"

}


service = CardSearchService()


result = service.search(
    card
)


print("=" * 40)
print("ABS CARD SEARCH SERVICE v1.3 DEBUG")
print("=" * 40)

print()

print(result)

print()

print("=" * 40)
