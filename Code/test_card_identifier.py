from recognition.feature_extractor import FeatureExtractor
from recognition.card_identifier import CardIdentifier

extractor = FeatureExtractor()


features = extractor.extract("database/images/base1-1.png")


identifier = CardIdentifier()


result = identifier.identify(features)


print(result)
