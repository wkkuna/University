set title "Multiplication time dependent on block size"
set datafile separator ','
set key autotitle columnhead
set ylabel "Time[s]"
set xlabel "n"
set yrange [0:12]
set style data lines
plot "../analisys/size_matters/diagram_files/1.csv" using 1:2 title "1", \
"../analisys/size_matters/diagram_files/2.csv" using 1:2 title "2", \
"../analisys/size_matters/diagram_files/4.csv" using 1:2 title "4", \
"../analisys/size_matters/diagram_files/8.csv" using 1:2 title "8", \
"../analisys/size_matters/diagram_files/16.csv" using 1:2 title "16", \
"../analisys/size_matters/diagram_files/32.csv" using 1:2 title "32", \
"../analisys/size_matters/diagram_files/64.csv" using 1:2 title "64", \
"../analisys/size_matters/diagram_files/128.csv" using 1:2 title "128"

