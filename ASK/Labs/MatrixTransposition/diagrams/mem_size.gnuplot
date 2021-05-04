set title "Transposition time comparison"
set datafile separator ','
set key autotitle columnhead
set colorsequence classic
set xrange [8:16256]
set ylabel "Time[s]"
set xlabel "KiB"
set style data lines
plot "../analisys/cache_size_experiment/mem_size_transpose0.csv" using 1:2 title "transpose0", \
"../analisys/cache_size_experiment/mem_size_transpose1.csv" using 1:2 title "transpose1"