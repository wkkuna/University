set title "Randwalk size impact on IPC"
set datafile separator ','
set key autotitle columnhead
set colorsequence classic
set ylabel "IPC"
set xlabel "Size [KiB]"
set xrange [0:1048576]
set style data lines
plot "../analysis/sizeTest/randwalk0.csv" using 1:2 title "randwalk0", \
    "../analysis/sizeTest/randwalk1.csv" using 1:2 title "randwalk1"