set title "transpose0: Trasposition time using different BLOCK value"
set datafile separator ','
set key autotitle columnhead
set colorsequence classic
set ylabel "Time[s]"
set xlabel "n"
set yrange [0:0.12]
set xrange [32:4096]
set style data lines
plot "../analisys/size_matters/transpose0_data/1.csv" using 1:2 title "1", \
"../analisys/size_matters/transpose0_data/2.csv" using 1:2 title "2", \
"../analisys/size_matters/transpose0_data/4.csv" using 1:2 title "4", \
"../analisys/size_matters/transpose0_data/8.csv" using 1:2 title "8", \
"../analisys/size_matters/transpose0_data/16.csv" using 1:2 title "16", \
"../analisys/size_matters/transpose0_data/32.csv" using 1:2 title "32", \
"../analisys/size_matters/transpose0_data/64.csv" using 1:2 title "64", \
"../analisys/size_matters/transpose0_data/128.csv" using 1:2 title "128"

