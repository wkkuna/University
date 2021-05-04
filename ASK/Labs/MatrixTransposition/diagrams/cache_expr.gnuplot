set title "Transposition time comparison"
set datafile separator ','
set key autotitle columnhead
set colorsequence classic
set ylabel "Time[s]"
set xlabel "n"
set yrange [0:4]
set xrange [32:16384]
set style data lines
plot "../analisys/cache_size_experiment/transpose0.csv" using 1:2 title "transpose0", \
"../analisys/cache_size_experiment/transpose1_8.csv" using 1:2 title "transpose1 BLOCK = 8", \
"../analisys/cache_size_experiment/transpose1_16.csv" using 1:2 title "transpose1 BLOCK = 16"