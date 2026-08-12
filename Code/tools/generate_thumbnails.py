# ============================================================
# ABS Thumbnail Generator v1.0
#
# Tworzy lekkie miniatury kart Pokemon
#
# Źródło:
# D:\ABS_DATA\POKEMON\TCG\EN
#
# Wynik:
# D:\ABS_DATA\POKEMON\THUMBNAILS
#
# NIE MODYFIKUJE ORYGINALNYCH PNG
# ============================================================


from pathlib import Path
from PIL import Image
import time

SOURCE = Path("D:/ABS_DATA/POKEMON/TCG/EN")

OUTPUT = Path("D:/ABS_DATA/POKEMON/THUMBNAILS")


# rozmiar dłuższego boku miniatury
MAX_SIZE = 300


JPEG_QUALITY = 85


def create_thumbnail(source_file, output_file):

    if output_file.exists():

        return "SKIP"

    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:

        with Image.open(source_file) as img:

            img = img.convert("RGB")

            img.thumbnail((MAX_SIZE, MAX_SIZE))

            img.save(output_file, "JPEG", quality=JPEG_QUALITY, optimize=True)

        return "OK"

    except Exception as e:

        print("ERROR:", source_file, e)

        return "ERROR"


def main():

    print("=" * 60)
    print("ABS Thumbnail Generator v1.0")
    print("=" * 60)

    start = time.time()

    files = list(SOURCE.rglob("*.png"))

    total = len(files)

    created = 0
    skipped = 0
    errors = 0

    print(f"Found images: {total}")

    print()

    for i, file in enumerate(files, 1):

        relative = file.relative_to(SOURCE)

        output_file = (OUTPUT / relative).with_suffix(".jpg")

        result = create_thumbnail(file, output_file)

        if result == "OK":

            created += 1

        elif result == "SKIP":

            skipped += 1

        else:

            errors += 1

        print(f"[{i}/{total}] " f"{file.name} " f"{result}")

    elapsed = time.time() - start

    print()
    print("=" * 60)
    print("THUMBNAIL BUILD COMPLETE")
    print("=" * 60)

    print(
        {
            "images": total,
            "created": created,
            "skipped": skipped,
            "errors": errors,
            "seconds": round(elapsed, 2),
        }
    )


if __name__ == "__main__":

    main()
