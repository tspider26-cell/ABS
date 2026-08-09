from recognition.feature_extractor import FeatureExtractor
from recognition.card_identifier import CardIdentifier

IMAGE = "scans/last_card.jpg"


extractor = FeatureExtractor()


print("ANALIZA OBRAZU:")
print(IMAGE)


features = extractor.extract(IMAGE)


if features is None:

    print("BŁĄD: nie można odczytać obrazu")

    exit()


print("\nCECHY:")
print(features)


identifier = CardIdentifier()


result = identifier.identify(features)


print("\nWYNIK ROZPOZNANIA:")
print(result)
