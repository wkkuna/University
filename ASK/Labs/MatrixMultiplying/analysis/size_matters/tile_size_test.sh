#!/bin/bash
# Simple script that collets data for specyfic
# block size

# When changing block parameter in script
# it is necessary to change it in matmult.h

pp="memory"
BLOCK=16
dir_raw=raw
dir_m=misses
dir_t=time
file=$BLOCK.txt
rm $dir_raw/*
cd ../..
make clean
make
cd analisys/size_matters
rm -dr $dir_raw/$BLOCK
mkdir $dir_raw/$BLOCK
for i in {64..2048..64}; do echo $i >> $dir_raw/$BLOCK/x_axis.txt\
&& ../../matmult -p $pp -n $i -v 3 >> $dir_raw/$BLOCK/$file; done

cat $dir_raw/$BLOCK/$file | grep -o '[0-9][0-9]*\.[0-9]*\%' > $dir_m/$file
python3 ../split.py $dir_m/$file  $dir_m/$BLOCK/
rm $dir_m/$file

cat $dir_raw/$BLOCK/$file | grep -o '[0-9]*\.[0-9]* ' > $dir_t/$file
