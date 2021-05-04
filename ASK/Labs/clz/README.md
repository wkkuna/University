Wiodąca liczba zer
===

W pliku `clz.s` zaprogramuj w asemblerze `x86-64` procedurę o sygnaturze
`int clz(uint64_t)`, która dla danego słowa maszynowego wyznacza długość
najdłuższego prefiksu składającego się z samych zer. Rozwiązanie ma działać w
`O(log n)`, gdzie `n` jest długością słowa maszynowego.

<sub>**UWAGA!** Można używać tylko i wyłącznie instrukcji poznanych na
wykładzie. Użycie instrukcji `lzcnt` lub podobnych jest niedozwolone!</sub>
