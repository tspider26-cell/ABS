from pathlib import Path
import json
from collections import Counter, defaultdict

INVENTORY = Path(r"D:\PTCG_FULL_DATABASE\logs\abs_image_inventory_v1.json")
DUPLICATES = Path(r"D:\PTCG_FULL_DATABASE\logs\image_duplicates_v1.json")

OUTPUT = Path(r"D:\PTCG_FULL_DATABASE\logs\abs_image_source_report_v1.json")


def detect_source(path):

    p = path.lower()

    if "serebii" in p:
        source = "SEREBII"
    elif "abs_data" in p:
        source = "ABS_DATA"
    else:
        source = "OTHER"

    if "\\english\\" in p or "\\en\\" in p:
        lang = "EN"
    elif "\\japanese\\" in p or "\\jp\\" in p:
        lang = "JP"
    elif "zh" in p or "tw" in p:
        lang = "ZH"

    else:
        lang = "UNKNOWN"

    return source, lang


def main():

    print("=" * 70)
    print("ABS DATABASE v2")
    print("IMAGE SOURCE ANALYZER v1")
    print("=" * 70)

    with open(INVENTORY, "r", encoding="utf-8") as f:
        inventory = json.load(f)

    with open(DUPLICATES, "r", encoding="utf-8") as f:
        duplicates = json.load(f)

    source_counter = Counter()
    language_counter = Counter()
    source_lang_counter = Counter()

    resolutions = Counter()

    examples = defaultdict(list)

    for img in inventory["images"]:

        path = img["file"]

        source, lang = detect_source(path)

        source_counter[source] += 1
        language_counter[lang] += 1
        source_lang_counter[f"{source}_{lang}"] += 1

        resolutions[f'{img["width"]}x{img["height"]}'] += 1

        if len(examples[source]) < 5:
            examples[source].append(path)

    report = {
        "total_images": inventory["total"],
        "duplicate_groups": len(duplicates),
        "sources": dict(source_counter),
        "languages": dict(language_counter),
        "source_languages": dict(source_lang_counter),
        "top_resolutions": resolutions.most_common(20),
        "examples": dict(examples),
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    print()
    print("TOTAL IMAGES:", inventory["total"])
    print("DUPLICATE GROUPS:", len(duplicates))

    print()
    print("SOURCES:")
    for k, v in source_counter.items():
        print(k, v)

    print()
    print("LANGUAGES:")
    for k, v in language_counter.items():
        print(k, v)

    print()
    print("OUTPUT:")
    print(OUTPUT)

    print("=" * 70)


if __name__ == "__main__":
    main()
