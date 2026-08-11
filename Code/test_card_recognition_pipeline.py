from services.card_recognition_pipeline import CardRecognitionPipeline


print("=" * 40)
print("ABS CARD RECOGNITION PIPELINE v3.1")
print("=" * 40)


pipeline = CardRecognitionPipeline()


result = pipeline.recognize(
    "scans/last_card.jpg"
)


print(result)


print("=" * 40)
