from services.card_identifier import CardIdentifier


metadata = {

    "family": "Pokemon",
    "number": "035/088",
    "set": "WL035"

}


service = CardIdentifier()

result = service.identify(
    metadata
)


print("=" * 40)
print("ABS CARD IDENTIFIER v1.0")
print("=" * 40)

print()

print(result)

print()

print("=" * 40)
