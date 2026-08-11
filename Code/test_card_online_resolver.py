from services.card_online_resolver import CardOnlineResolver

metadata = {
    "family": "Pokemon",
    "name": "Spritzee",
    "set": "Perfect Order",
    "code": "POR",
    "number": "035/088",
    "language": "EN",
}


resolver = CardOnlineResolver()


result = resolver.resolve(metadata)


print("=" * 40)
print("ABS CARD ONLINE RESOLVER v1.0")
print("=" * 40)

print()

print(result)

print()

print("=" * 40)
