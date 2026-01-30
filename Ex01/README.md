# 📊 Analiza statystyczna języka czeskiego (NLP)

Projekt realizuje podstawowe etapy **statystycznego przetwarzania języka naturalnego (NLP)** dla języka czeskiego.  
Celem jest zbadanie rozkładu częstości słów, weryfikacja prawa Zipfa oraz identyfikacja rdzenia języka na podstawie grafu współwystępowania.

---

## 📚 Wykorzystane teksty

Korpus został zbudowany z czterech czeskich książek pochodzących z **Project Gutenberg** i połączonych w jeden zbiór tekstowy (~100 000 słów):

1. **Blesky nad Beskydami** — František Omelka  
2. **Cvičení maličkých ve svatém náboženství křesťansko-katolickém** — Peregrin Obdržálek  
3. **Štafeta** — František Omelka  
4. **Vlci proti Mustangům** — František Omelka  

Teksty zostały wstępnie oczyszczone z nagłówków, licencji i metadanych.

---

## ⚙️ Zakres analizy

Projekt obejmuje następujące kroki:

- wczytanie i tokenizacja tekstu  
- utworzenie tabeli częstości słów  
- analiza rozkładu częstości (rank–frequency)  
- weryfikacja prawa Zipfa (`r × f ≈ const`)  
- wizualizacja wykresów (log–log)  
- budowa grafu współwystępowania słów  
- identyfikacja rdzenia języka na podstawie stopni węzłów  

---

## 📈 Wyniki

- Rozkład częstości słów jest zgodny z prawem Zipfa, szczególnie dla słów o wyższych rangach.  
- Iloczyn rangi i częstości stabilizuje się od ok. 1000 pozycji.  
- Najbardziej połączone węzły w grafie odpowiadają słowom funkcyjnym języka czeskiego.  
- Rdzeń języka tworzy gęstą sieć powiązań gramatycznych.

---

## 🛠️ Wymagania

- Python 3.x  
- Biblioteki: `re`, `collections`, `numpy`, `matplotlib`, `networkx`  

Projekt został wykonany w środowisku **Jupyter Notebook**.

---

## 📄 Pliki

- `NLP_ex01.ipynb` — główny notebook z analizą  
- `README.md` — dokumentacja projektu  
- `czech-text.txt` — tekst poddawany analizie statystycznej

---

## 🎯 Cel dydaktyczny

Projekt demonstruje, w jaki sposób **proste metody statystyczne** pozwalają analizować strukturę języka naturalnego bez użycia zaawansowanych narzędzi NLP.
