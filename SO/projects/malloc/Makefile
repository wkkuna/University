CC = gcc -g
CFLAGS = -O3 -Wall -Werror -DDRIVER

OBJS = mdriver.o mm.o memlib.o fsecs.o fcyc.o clock.o ftimer.o

all: mdriver

mdriver: $(OBJS)
	$(CC) $(CFLAGS) -o mdriver $(OBJS)

test: mdriver
	./mdriver -V -D

t: test.c mm.o memlib.o memlib.h mm.h
	$(CC) $(CFLAGS) -o t.elf test.c mm.o memlib.o

t1: t
	./t.elf

mdriver.o: mdriver.c fsecs.h fcyc.h clock.h memlib.h config.h mm.h
memlib.o: memlib.c memlib.h
mm.o: mm.c mm.h memlib.h
fsecs.o: fsecs.c fsecs.h config.h
fcyc.o: fcyc.c fcyc.h
ftimer.o: ftimer.c ftimer.h config.h
clock.o: clock.c clock.h

format:
	clang-format --style=file -i *.c *.h


clean:
	rm -f *~ *.o mdriver

.PHONY: all format archive clean
