from services.tcgdex_downloader import TCGdexDownloaderV2

# Tutaj wpiszemy właściwy adres TCGdex
SOURCE_URL = ""


downloader = TCGdexDownloaderV2(SOURCE_URL)


result = downloader.download()


print("=" * 40)
print("ABS TCGDEX DOWNLOADER v2.0")
print("=" * 40)

print()

print(result)

print()

print("=" * 40)
