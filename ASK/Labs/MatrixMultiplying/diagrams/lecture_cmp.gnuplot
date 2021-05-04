set title "Replicated lecture's experiment"
set datafile separator ','
set key autotitle columnhead
set yrange [0:50]
set xrange [32:700]
set ylabel "Cycles per iteration"
set xlabel "n"
set key autotitle columnhead
set style data linespoints
plot '../analisys/lecture_cmp/data.csv' using 1:2 with linespoints,\
'' using 1:3 with linespoints, '' using 1:4 with linespoints

