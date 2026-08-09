import json
import os

from recognition.feature_matcher_v21 import FeatureMatcherV21

PROFILE = "database/cards/my_first_card/profile.json"

TEST_IMAGE = "scans/last_card.jpg"


matcher = FeatureMatcherV21()


print("\nDIAGNOSTYKA PROFILU KARTY")
print("==========================")


with open(PROFILE, "r", encoding="utf-8") as f:

    profile = json.load(f)


results = []


for ref in profile["references"]:

    image = ref["image"]

    score = matcher.compare(TEST_IMAGE, image)

    result = {"reference": image, "score": int(score)}

    results.append(result)

    print(result)


results.sort(key=lambda x: x["score"], reverse=True)


print("\nNAJLEPSZA REFERENCJA:")
print(results[0])


print("\nPROFIL:")
print(profile["id"])
