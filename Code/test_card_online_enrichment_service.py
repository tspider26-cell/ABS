from services.card_online_enrichment_service import CardOnlineEnrichmentService


card = {

    "family": "Pokemon",
    "name": "Spritzee",
    "set": "Perfect Order",
    "code": "POR",
    "number": "035/088",
    "rarity": "Common",
    "language": "EN"

}


service = CardOnlineEnrichmentService()

result = service.enrich(card)


print("=" * 40)
print("ABS CARD ONLINE ENRICHMENT SERVICE v1.0")
print("=" * 40)

print()

print(result)

print()

print("=" * 40)
