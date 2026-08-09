from recognition.feature_extractor import FeatureExtractor

extractor = FeatureExtractor()


card = "database/images/base1-1.png"


features = extractor.extract(card)


print("CECHY KARTY:")
print(features)


extractor.save_features("base1-1", features)
