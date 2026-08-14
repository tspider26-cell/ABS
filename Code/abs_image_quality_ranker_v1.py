from pathlib import Path
import json

BASE = Path(r"D:\PTCG_FULL_DATABASE")

INDEX = BASE / "database" / "image_master_index.json"

OUTPUT = BASE / "database" / "image_master_index_ranked.json"


def source_score(source):

    scores = {
        "SEREBII_EN": 100,
        "SEREBII_JP": 100,
        "SEREBII_ROOT": 90,
        "ABS_DATA_EN": 75,
        "ABS_DATA_JP": 75,
        "ABS_DATA_ZH": 70,
        "TCGDEX": 65,
        "ABS_DATA_JP_ARCHIVE": 40,
    }

    return scores.get(source, 10)


def resolution_score(width, height):

    if not width or not height:
        return 0

    pixels = width * height

    if pixels >= 1000000:
        return 20

    if pixels >= 700000:
        return 15

    if pixels >= 500000:
        return 10

    return 5


def calculate_score(img):

    return source_score(img.get("source")) + resolution_score(
        img.get("width"), img.get("height")
    )


def main():

    print("=" * 70)
    print("ABS DATABASE v2")
    print("IMAGE QUALITY RANKER v1")
    print("=" * 70)

    with open(INDEX, "r", encoding="utf-8") as f:

        data = json.load(f)

    cards = data["cards"]

    total = 0

    for key, images in cards.items():

        for img in images:

            img["quality_score"] = calculate_score(img)

            total += 1

        images.sort(key=lambda x: x["quality_score"], reverse=True)

    with open(OUTPUT, "w", encoding="utf-8") as f:

        json.dump(data, f, indent=2, ensure_ascii=False)

    print()
    print("CARDS:", len(cards))
    print("IMAGES RANKED:", total)

    print()
    print("OUTPUT:")
    print(OUTPUT)

    print("=" * 70)


if __name__ == "__main__":
    main()
