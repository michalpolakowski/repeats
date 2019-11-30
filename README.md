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

#### Oczekiwania po refaktoryzacji
* Zmiana struktury kodu, by był bliższy programowaniu obiektowemu.
* Czytelność oraz łatwość utrzymania kodu będzie wyższa.
* Funkcjonalność programu pozostanie taka sama.

#### Metryki:
* Indeks dostępności: 74.85
* Złożoność cyklomatyczna: 6
* Sprzężenie klas: brak (interesujący nas fragment kodu składa się na razie z funkcji)
* Wiersze kodu: 84
