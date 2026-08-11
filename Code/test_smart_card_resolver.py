from services.smart_card_resolver import SmartCardResolver


print("=" * 40)
print("ABS SMART CARD RESOLVER v1.0")
print("=" * 40)


resolver = SmartCardResolver()


metadata = {
    "code": "POR",
    "number": "035/088",
    "set_id": "me03",
    "number": "035"
}


result = resolver.resolve(metadata)

print(result)

print("=" * 40)
