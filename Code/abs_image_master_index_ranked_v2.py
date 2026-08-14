from pathlib import Path
import json

SOURCE = Path(r"D:\PTCG_FULL_DATABASE\database\image_master_index.json")

OUTPUT = Path(r"D:\PTCG_FULL_DATABASE\database\image_master_index_ranked_v2.json")


def calculate_quality(img):

    score = 0

    width = img.get("width") or 0
    height = img.get("height") or 0

    source = img.get("source") or ""

    # rozdzielczość
    if height >= 1200:
        score += 20
    elif height >= 1000:
        score += 15
    elif height >= 900:
        score += 10

    if width >= 700:
        score += 10

    # priorytet źródła

    if source == "SEREBII_EN":
        score += 60

    elif source == "SEREBII_JP":
        score += 60

    elif source == "TCGDEX":
        score += 30

    elif source.startswith("ABS_DATA"):
        score += 20

    elif source.startswith("SEREBII"):
        score += 40

    return score


def main():

    print("=" * 70)
    print("ABS DATABASE v2")
    print("IMAGE MASTER INDEX RANKED BUILDER v2")
    print("=" * 70)

    with open(SOURCE, "r", encoding="utf-8") as f:

        data = json.load(f)

    cards = data["cards"]

    result = {"created": "ranked_v2", "cards": {}}

    total_images = 0

    for card_id, images in cards.items():

        ranked = []

        for img in images:

            item = dict(img)

            # zachowanie oryginalnej ścieżki
            if "path" in item:
                item["file"] = item["path"]

            item["quality_score"] = calculate_quality(item)

            ranked.append(item)

        ranked.sort(key=lambda x: x["quality_score"], reverse=True)

        for index, img in enumerate(ranked, start=1):

            img["rank"] = index

            img["preferred"] = index == 1

        result["cards"][card_id] = ranked

        total_images += len(ranked)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT, "w", encoding="utf-8") as f:

        json.dump(result, f, indent=2, ensure_ascii=False)

    print()
    print("CARDS:", len(result["cards"]))
    print("IMAGES:", total_images)
    print()
    print("OUTPUT:")
    print(OUTPUT)
    print("=" * 70)


if __name__ == "__main__":
    main()
