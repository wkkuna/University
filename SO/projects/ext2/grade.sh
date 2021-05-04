#!/bin/sh

IMAGE=debian9-ext2

if [ -d "/__w" ]; then
  ln -s /$IMAGE.img $IMAGE.img
  ln -s /$IMAGE.kern.log $IMAGE.kern.log
fi

sort $IMAGE.kern.log > $IMAGE.log
./ext2list test | sort > $IMAGE.user.log
diff -U 0 $IMAGE.log $IMAGE.user.log | \
  wdiff -d - | sed -e '1d;/^@@/d' > $IMAGE.log.diff
if [ -s $IMAGE.log.diff ]; then
  echo "First 100 differences:"
  head -n 100 $IMAGE.log.diff
fi
INCORRECT=$(cat $IMAGE.log.diff | wc -l)
ALL=$(cat $IMAGE.log | wc -l)
echo "\nIncorrect files: $INCORRECT/$ALL"
exit $(($INCORRECT > 0))
