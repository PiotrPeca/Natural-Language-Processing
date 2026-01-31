# Učíme se česky - Interaktywny kreator zdań czeskich

Aplikacja webowa do nauki gramatyki języka czeskiego poprzez budowanie zdań prostych (SVO - Subject-Verb-Object).

## Opis

Program prowadzi użytkownika krok po kroku przez proces tworzenia poprawnych gramatycznie zdań w języku czeskim. Interfejs jest intuicyjny i łatwy w nawigacji.

### Funkcjonalności

**Budowanie podmiotu (Subjekt):**
- Wybór rzeczownika z listy (~50 słów z tłumaczeniami)
- Liczba pojedyncza / mnoga
- Opcjonalne określniki:
  - Zaimki wskazujące (ten, tento, tamten)
  - Zaimki dzierżawcze (můj, tvůj, jeho, její, náš, váš, jejich)
  - Przymiotniki (~40 słów)

**Wybór czasownika (Sloveso):**
- Lista ~40 czasowników z tłumaczeniami
- Osoba (1., 2., 3.) i liczba (sg/pl)
- Czas: teraźniejszy, przeszły, przyszły
- Tryb: oznajmujący, rozkazujący, przypuszczający
- Forma: twierdząca/przecząca, pytanie

**Dopełnienie (Objekt) - opcjonalne:**
- Te same opcje co dla podmiotu
- Automatyczna odmiana przez akuzativ

## Instalacja

```bash
cd Ex02
pip install -r requirements.txt
```

## Uruchomienie

```bash
python app.py
```

Aplikacja będzie dostępna pod adresem: http://localhost:5000

## Technologie

- **Backend:** Python + Flask
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Styl:** Nowoczesny dark theme z gradientami

## Struktura projektu

```
Ex02/
├── app.py              # Backend Flask + logika gramatyczna
├── static/
│   └── index.html      # Frontend (HTML + CSS + JS)
├── requirements.txt    # Zależności Python
└── README.md           # Dokumentacja
```

## Gramatyka czeska

### Rodzaje rzeczowników
- **Męski żywotny** (m_zyw): muž, student, otec...
- **Męski nieżywotny** (m_nzyw): hrad, dům, stůl...
- **Żeński** (f): žena, kniha, škola...
- **Nijaki** (n): město, okno, dítě...

### Odmiana przez przypadki
Aplikacja obsługuje:
- **Nominativ** - dla podmiotu
- **Akuzativ** - dla dopełnienia bliższego

### Koniugacja czasowników
Obsługiwane klasy:
- Regularne: -at, -ovat, -it, -et/-ět
- Nieregularne: být, mít, chtít, muset, moct, vědět, jíst, pít, spát, číst, žít

## Przykłady zdań

- "Dobrý student čte knihu." (Dobry student czyta książkę.)
- "Moje sestra miluje hudbu." (Moja siostra kocha muzykę.)
- "Starý učitel nepracuje." (Stary nauczyciel nie pracuje.)

## Cel dydaktyczny

Aplikacja demonstruje, jak wykorzystać proste reguły gramatyczne do automatycznego generowania poprawnych zdań w języku czeskim, pomagając w nauce odmiany rzeczowników, przymiotników i koniugacji czasowników.
