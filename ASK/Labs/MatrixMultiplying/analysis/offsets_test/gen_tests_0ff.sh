#!/bin/bash
# Script that generates 
pp="memory"
offsets="2-1-0"
dir_raw=raw
dir_m=misses
dir_t=time
dir=offsets_test
f0=0.txt
f1=1.txt
f2=2.txt
f3=3.txt
rm -rd $dir_raw/$offsets
cd ../..
make clean
make
cd analisys/offsets_test/
mkdir $dir_raw/$offsets
for i in {64..2048..64}; do echo $i >> $dir_raw/$offsets/x_axis.txt\
&& ../../matmult -p $pp -n $i -v 0 >> $dir_raw/$offsets/$f0\
&& ../../matmult -p $pp -n $i -v 1 >> $dir_raw/$offsets/$f1\
&& ../../matmult -p $pp -n $i -v 2 >> $dir_raw/$offsets/$f2\
&& ../../matmult -p $pp -n $i -v 3 >> $dir_raw/$offsets/$f3; done
rm -rd $dir_m/$offsets
mkdir $dir_m/$offsets

cat $dir_raw/$offsets/$f0 | grep -o '[0-9][0-9]*\.[0-9]*\%' > $dir_m/$offsets/$f0
python3 ../split.py $dir_m/$offsets/$f0  $dir_m/$offsets/0
rm $dir_m/$offsets/$f0

cat $dir_raw/$offsets/$f1 | grep -o '[0-9][0-9]*\.[0-9]*\%' > $dir_m/$offsets/$f1
python3 ../split.py $dir_m/$offsets/$f1 $dir_m/$offsets/1
rm $dir_m/$offsets/$f1

cat $dir_raw/$offsets/$f2 | grep -o '[0-9][0-9]*\.[0-9]*\%' > $dir_m/$offsets/$f2
python3 ../split.py $dir_m/$offsets/$f2  $dir_m/$offsets/2
rm $dir_m/$offsets/$f2

cat $dir_raw/$offsets/$f3 | grep -o '[0-9][0-9]*\.[0-9]*\%' > $dir_m/$offsets/$f3
python3 ../split.py $dir_m/$offsets/$f3  $dir_m/$offsets/3
rm $dir_m/$offsets/$f3

rm -rd $dir_t/$offsets
mkdir $dir_t/$offsets
cat $dir_raw/$offsets/$f0 | grep -o '[0-9]*\.[0-9]* ' > $dir_t/$offsets/$f0
cat $dir_raw/$offsets/$f1 | grep -o '[0-9]*\.[0-9]* ' > $dir_t/$offsets/$f1
cat $dir_raw/$offsets/$f2 | grep -o '[0-9]*\.[0-9]* ' > $dir_t/$offsets/$f2
cat $dir_raw/$offsets/$f3 | grep -o '[0-9]*\.[0-9]* ' > $dir_t/$offsets/$f3
