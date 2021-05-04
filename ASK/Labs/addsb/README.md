Dodawanie z nasyceniem
===

Zaimplementuj algorytm dodawania z nasyceniem dwóch ośmioelementowych wektorów
liczb typu `int8_t` składowanych w słowach maszynowych o typie `uint64_t`.
W arytmetyce z nasyceniem dla wartości typu `int8_t` zachodzi `80 + 60 = 127`,
a `(−40) + (−100) = −128`.

### Ważne

1. Można używać wyłącznie instrukcji arytmetyczno-logicznych poznanych na
   wykładzie i ćwiczeniach.
2. Użycie instrukcji sterujących (poza `ret`) oraz `cmov` i `set` jest
   niedozwolone!
3. Modyfikowanie innych plików niż `addsb.s` jest niedozwolone!
