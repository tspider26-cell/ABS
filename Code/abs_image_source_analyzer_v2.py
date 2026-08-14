from pathlib import Path
import json
from collections import Counter, defaultdict

INPUT = Path(r"D:\PTCG_FULL_DATABASE\logs\abs_image_inventory_v1.json")

OUTPUT = Path(r"D:\PTCG_FULL_DATABASE\logs\abs_image_source_report_v2.json")


def detect_source(path):

    p = path.lower()

    # SEREBII
    if "ptcg_full_database\\images\\serebii" in p:

        if "\\english\\" in p:
            return "SEREBII_EN"

        if "\\japanese\\" in p:
            return "SEREBII_JP"

        return "SEREBII_ROOT"

    # ABS_DATA
    if "abs_data\\pokemon\\tcg" in p:

        if "\\en\\" in p:
            return "ABS_DATA_EN"

        if "\\jp\\" in p:
            return "ABS_DATA_JP"

        if "zh-tw" in p:
            return "ABS_DATA_ZH"

        if "jp_archive_old" in p:
            return "ABS_DATA_JP_ARCHIVE"

        return "ABS_DATA_OTHER"

    # TCGDEX
    if "pokemon_images\\tcgdex" in p:
        return "TCGDEX"

    return "OTHER"


def main():

    print("=" * 70)
    print("ABS DATABASE v2")
    print("IMAGE SOURCE ANALYZER v2")
    print("=" * 70)

    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    sources = Counter()
    examples = defaultdict(list)
    resolutions = Counter()

    for img in data["images"]:

        path = img["file"]

        source = detect_source(path)

        sources[source] += 1

        resolutions[f'{img["width"]}x{img["height"]}'] += 1

        if len(examples[source]) < 5:
            examples[source].append(path)

    report = {
        "total_images": data["total"],
        "sources": dict(sources),
        "top_resolutions": resolutions.most_common(20),
        "examples": dict(examples),
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:

        json.dump(report, f, indent=4, ensure_ascii=False)

    print()
    print("TOTAL:", data["total"])

    print()
    print("SOURCES:")

    for k, v in sources.items():
        print(f"{k}: {v}")

    print()
    print("OUTPUT:")
    print(OUTPUT)

    print("=" * 70)


if __name__ == "__main__":
    main()
