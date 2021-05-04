Odwracanie wektora bitów
===

W pliku `bitrev.s` zaprogramuj w asemblerze `x86-64` procedurę o sygnaturze
`uint64_t bitrev(uint64_t)`. Dla danego słowa maszynowego składającego się z
bitów <tt>b<sub>n-1</sub>...b<sub>0</sub></tt> procedura ma wyznaczyć jego
lustrzane odbicie tak, że dla każdego `i` zachodzi <tt>r<sub>i</sub> =
b<sub>(n-1)-i</sub></tt>, gdzie `r` jest wynikiem działania. Rozwiązanie ma
działać w `O(log n)`, gdzie `n` jest długością słowa maszynowego w bitach.


### Ważne

1. Można używać wyłącznie instrukcji arytmetyczno-logicznych poznanych na
   wykładzie i ćwiczeniach.
2. Użycie instrukcji `bswap` i instrukcji sterujących (poza `ret`) jest
   niedozwolone!
3. Modyfikowanie innych plików niż `bitrev.s` jest niedozwolone!
