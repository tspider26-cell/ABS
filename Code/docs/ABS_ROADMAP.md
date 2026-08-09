# ABS - Artysta Booster Scanner

## Wizja projektu

ABS jest uniwersalnym skanerem kart kolekcjonerskich.

Nie tylko Pokemon.

Obsługiwane docelowo:

- Pokemon TCG
- Magic The Gathering
- Yu-Gi-Oh!
- One Piece Card Game
- Lorcana
- Sport Cards
- inne kolekcje


# AKTUALNY STAN PROJEKTU

## ABS v0.1

Gotowe:

✅ Kamera działa

✅ Wykrywanie karty

✅ ROI

✅ Auto Capture

✅ Zapis last_card.jpg

✅ Połączenie z TCGdex

✅ Pobieranie obrazów kart

✅ Lokalna baza obrazów

✅ Pierwszy matcher ORB


# AKTUALNY CEL

Nie budujemy jeszcze pełnego AI.

Najpierw tworzymy stabilny silnik identyfikacji.


# ETAP 1 - Vision

Cel:

Przygotowanie idealnego obrazu karty.

Kolejność:

1. Card Detection

2. Card Rectification

3. Normalizacja obrazu


Status:

🟡 W trakcie


# ETAP 2 - Recognition Engine

Cel:

Rozpoznanie konkretnej karty.

Moduły:

- Feature Extractor
- Hash Generator
- ORB/SIFT Matcher
- Card Identifier


Status:

⏳ Plan


# ETAP 3 - Database Engine

Cel:

Baza kart.

Struktura:

Pokemon

Magic

Yu-Gi-Oh

inne


Dane:

- nazwa
- numer
- seria
- język
- wariant
- obraz
- cena


Status:

⏳ Plan


# ETAP 4 - Variant Recognition

Rozpoznawanie:

- holo
- reverse holo
- promo
- pierwsza edycja
- język
- wydanie


Status:

⏳ Plan


# ETAP 5 - Market Module

Informacje:

- ceny
- historia
- trendy
- wartość kolekcji


Status:

⏳ Plan


# ZASADA PROJEKTU

Nie skaczemy między etapami.

Najpierw kończymy aktualny etap.

Pomysły zapisujemy tutaj.

Kodujemy tylko aktualny krok.


# NAJBLIŻSZY KROK

Card Rectifier

Cel:

last_card.jpg

↓

wyprostowana karta

↓

lepsze rozpoznawanie