# ARCHITECTURE

## Architektura projektu

Artysta Break Studio został zaprojektowany jako aplikacja modułowa.

Każdy moduł odpowiada wyłącznie za swoje zadanie.

---

## ABS Core

Odpowiada za:

- uruchamianie programu,
- konfigurację,
- logowanie,
- komunikację pomiędzy modułami.

---

## ABS Vision

Odpowiada za:

- obsługę kamer,
- analizę obrazu,
- wykrywanie kart,
- przygotowanie obrazu do AI.

---

## ABS Recognition

Odpowiada za:

- rozpoznawanie kart,
- odczyt numerów,
- identyfikację zestawów.

---

## ABS Market

Odpowiada za:

- pobieranie cen,
- analizę rynku,
- historię cen.

---

## ABS Overlay

Odpowiada za:

- wyświetlanie informacji,
- integrację z OBS,
- animacje.

---

## ABS Archive

Odpowiada za:

- historię otwarć,
- zapis sesji,
- eksport danych.

---

## ABS Analytics

Odpowiada za:

- statystyki,
- raporty,
- analizę danych.

---

# Zasady projektu

Każdy moduł powinien być niezależny.

Kod powinien być prosty, czytelny i możliwy do rozbudowy.