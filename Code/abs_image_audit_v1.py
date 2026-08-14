import os
import json
import hashlib
from PIL import Image
from pathlib import Path
from datetime import datetime

ROOTS = [
    r"D:\PTCG_FULL_DATABASE\images",
    r"D:\ABS_DATA\Pokemon\TCG",
    r"D:\ABS_DATA\pokemon_images",
]


OUTPUT = r"D:\PTCG_FULL_DATABASE\logs"


def sha256(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


def scan_file(path):

    try:
        size = os.path.getsize(path)

        width = None
        height = None
        fmt = None

        try:
            with Image.open(path) as im:
                width, height = im.size
                fmt = im.format
        except:
            pass

        parts = Path(path).parts

        return {
            "file": str(path),
            "extension": Path(path).suffix.lower(),
            "bytes": size,
            "width": width,
            "height": height,
            "format": fmt,
            "hash": sha256(path),
        }

    except Exception as e:
        return {"file": str(path), "error": str(e)}


def main():

    print("=" * 70)
    print("ABS DATABASE v2")
    print("IMAGE INVENTORY AUDIT v1")
    print("=" * 70)

    results = []

    for root in ROOTS:

        print("\nSCAN:", root)

        if not os.path.exists(root):
            print("MISSING")
            continue

        for dirpath, dirs, files in os.walk(root):

            for f in files:

                if f.lower().endswith((".jpg", ".jpeg", ".png")):

                    path = os.path.join(dirpath, f)

                    results.append(scan_file(path))

                    if len(results) % 1000 == 0:
                        print("FILES:", len(results))

    os.makedirs(OUTPUT, exist_ok=True)

    inventory = os.path.join(OUTPUT, "abs_image_inventory_v1.json")

    with open(inventory, "w", encoding="utf8") as f:
        json.dump(
            {
                "created": datetime.now().isoformat(),
                "total": len(results),
                "images": results,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    hashes = {}

    for x in results:

        h = x.get("hash")

        if h:
            hashes.setdefault(h, []).append(x["file"])

    duplicates = {h: v for h, v in hashes.items() if len(v) > 1}

    dupfile = os.path.join(OUTPUT, "image_duplicates_v1.json")

    with open(dupfile, "w", encoding="utf8") as f:
        json.dump(duplicates, f, indent=2, ensure_ascii=False)

    print()
    print("=" * 70)
    print("COMPLETE")
    print("TOTAL IMAGES:", len(results))
    print("DUPLICATE GROUPS:", len(duplicates))
    print()
    print(inventory)
    print(dupfile)
    print("=" * 70)


if __name__ == "__main__":
    main()
