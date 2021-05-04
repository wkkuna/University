Reszta z dzielenia przez 17
===
W pliku `mod17.s` zaprogramuj w asemblerze `x86-64` procedurę o sygnaturze
`int mod17(uint64_t)`, która liczy resztę z dzielenia danej liczby przez 17.
Cała trudność zadania polega na tym, że rozwiązanie **nie może** używać
instrukcji mnożenia ani dzielenia.

<sub>*Wskazówka:* Przypomnij sobie następującą własność reszty z dzielenia
przez 11: różnica sum cyfr (dziesiętnych) na parzystych i nieparzystych
pozycjach ma taką samą resztę z dzielenia przez 11 co cała liczba, np.
reszta z dzielenia 183716 przez 11 to 5, bo (8+7+6)-(1+3+1) = 16, a reszta
z dzielenia 16 przez 11 to właśnie 5. Okazuje się, że analogiczna własność
zachodzi w dowolnym systemie pozycyjnym, np. w systemie szesnastkowym łatwo
liczy się resztę z dzielenia przez 17.</sub>

<sub>**UWAGA!** Można używać tylko instrukcji poznanych na wykładzie,
z wyłączeniem instrukcji mnożenia, dzielenia i podobnych.
Użycie instrukcji `div` lub `idiv` jest niedozwolone!</sub>
