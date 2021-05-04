set title "Randwalk execution time"
set datafile separator ','
set key autotitle columnhead
set colorsequence classic
set ylabel "Time[s]"
set xlabel "Size [KiB]"
set xrange [0:1048576]
set style data lines
plot "../analysis/sizeTest/time.csv" using 1:2 title "randwalk0", \
"../analysis/sizeTest/time.csv" using 1:3 title "randwalk1"