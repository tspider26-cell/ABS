from services.smart_online_resolver import SmartOnlineResolver


card = {

    "family": "Pokemon",
    "name": "Spritzee",
    "set": "Perfect Order",
    "code": "POR",
    "number": "035/088",
    "rarity": "Common",
    "language": "EN"

}


service = SmartOnlineResolver()

result = service.resolve(card)


print("=" * 40)
print("ABS SMART ONLINE RESOLVER v1.0")
print("=" * 40)

print()

print(result)

print()

print("=" * 40)
