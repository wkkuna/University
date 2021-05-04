set title "2-1-0 offset"
set datafile separator ','
set ylabel "Time[s]"
set xlabel "n"
set style data lines
plot "../analisys/offsets_test/data2.csv" using 1:2 title "matmult0", \
"../analisys/offsets_test/data2.csv" using 1:3 title "matmult1", \
"../analisys/offsets_test/data2.csv" using 1:4 title "matmult2", \
"../analisys/offsets_test/data2.csv" using 1:5 title "matmult3"
