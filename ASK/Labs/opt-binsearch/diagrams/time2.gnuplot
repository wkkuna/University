set title "Binsearch execution time before and after builtin prefetch"
set datafile separator ','
set key autotitle columnhead
set colorsequence classic
set ylabel "Time[s]"
set xlabel "Size [KiB]"
set xrange [0:1099511627776]
set style data lines
plot "../analysis/prefetch/time.csv" using 1:2 title "before", \
"../analysis/prefetch/time.csv" using 1:3 title "after"