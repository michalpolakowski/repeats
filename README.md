# Refaktoryzacja stockyard-files

## Założenia projektu
Kod do refaktoryzacji został napisany w języku Python na podstawie fragmentu kodu z prywatnego projektu.
Celem tego peojektu była refaktoryzacja tego kodu.

## Opis programu
Przedstawiony fragment kodu ma za zadanie wygenerować pliki zawierające nazwy próbek, które zostały powtórzone. Każdy plik posiada okresloną ilość nazw, którą możemy zmienić w ustawieniach. Krokiem poprzedzającym generowanie plików jest pobranie z bazy danych powtórzonych próbek, które zostały dodane danego dnia.
Na potrzeby sprawnego testowania programu musiała zostac zaimplementowana cała struktura djangowego projektu, natomiast fragment kodu, którego dotyczyć bedzie refaktoryzacja znajduje się w folderze stockyard/utils w pliku stockyard_files.py.

## Klasy programu
* Klasa Repeat (powtórzenie) Repeat to klasa rzutująca strukturę obiektu na wpis w bazie danych (wykorzystane Django ORM)
* Klasa Laboratory (laboratorium) reprezentuje laboratorium z którego pobierane są próbki

## Testy
Dla przedstawionego kodu dołączony jest test sprawdzający czy refaktoryzowany fragment poprawnie wykonuje swoje zadanie.
* StockyardFilesTestCase

## Refaktoryzacja

### Wersja 0
Wersja 0 to początkowa wersja kodu, która będzie poddawana dalszym obróbkom.

#### Wnioski:
* Należy przepisać sposób pobierania danych z bazy danych, gdyż występuje tam fragment kodu, który jest powtórzony trzykrotnie z jedynie innym napisem wejściowym.
* Należy zasotosować Programowanie Obiektowe.
* Rozbicie funkcji na kilka metod, które będą wykonywać konkretne zadania wewnątrz obiektu.
* Kod musi być bardziej pythonowy, gdyż osoba pisząca go wczesniej musiała na codzień uzywać innego języka programowania.
* Istnieją fragmenty kodu, które się powtarzają, trzeba je przenieść do wydzielonych funkcji.

#### Oczekiwania po refaktoryzacji
* Zmiana struktury kodu, by był bliższy programowaniu obiektowemu.
* Czytelność oraz łatwość utrzymania kodu będzie wyższa.
* Funkcjonalność programu pozostanie taka sama.
* Fragmenty kodu nie będą się powtarzać.

#### Metryki:
* Indeks dostępności: 57.54
* Złożoność cyklomatyczna: generate_stockyard_split_repeats_files - B (8), generate_stockyard_repeats_files - B (6)
* Sprzężenie klas: brak (interesujący nas fragment kodu składa się na razie z funkcji)
* Wiersze kodu: 165

---
### Wersja 1

#### Dokonane refaktoryzacje:
* Iteracje zmienione są w taki sposób, że zamiast inicjalizacji indeksu i jego zmieniania używamy wbudowanej funkcji enumerate.
* Zmieniona jest forma zapisu filtra danych z bazy danych.

#### Metryki:
* Indeks dostępności: 57.47
* Złożoność cyklomatyczna: generate_stockyard_split_repeats_files - B (9), generate_stockyard_repeats_files - B (7)
* Sprzężenie klas: brak (interesujący nas fragment kodu składa się na razie z funkcji)
* Wiersze kodu: 165

---
### Wersja 2

#### Dokonane refaktoryzacje:
* Całość została przepisana według kanonu programowania obiektowego.
* Z kodu zostały usuniętę większe powtórzenia.
* Ze względu na zamianę funkcji na klasę delikatnej modyfikacji musiały ulec również testy.

#### Metryki:
* Indeks dostępności: 64.25
* Złożoność cyklomatyczna: StockyardRepeatsFilesGenerator - A (3)
* Sprzężenie klas: StockyardRepeatsFilesGenerator - 24
* Wiersze kodu: 147

--- 
### Wersja ∞

#### Dokonane refaktoryzacje:
* dodanie typowania

#### Metryki:
- Indeks dostępności: 64.05
- Złożoność cyklomatyczna: 3
- Sprzężenie klas: 25
- Wiersze kodu: 148