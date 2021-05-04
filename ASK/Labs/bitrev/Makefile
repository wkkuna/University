CC = gcc -g -no-pie
CFLAGS = -Og -Wall
LDFLAGS = 
ASFLAGS = -g

# Configurable parameters
PROCEDURE ?= bitrev.s:bitrev
ILIMIT ?= 48
MAXSIZE ?= 256
BADINSNS ?= 'bswap,j*,call*'
MINIPC ?= 1.87

MAXINSNS = $(ILIMIT)

CHECK = ./check-solution --procedure $(PROCEDURE) \
	                 --max-size $(MAXSIZE) --bad-insns $(BADINSNS)
RUN = ./run-solution --procedure $(PROCEDURE) \
                     --max-insns $(MAXINSNS) -- ./main
INSTALL = sudo apt-get install -q=2 --no-install-recommends

.packages:
	 $(INSTALL) valgrind llvm-8
	 touch $@

check: .packages main
	$(CHECK)

main: main.o bitrev.o
	$(CC) $(LDFLAGS) -o $@ $^

test-1: check
	$(RUN) 0x0123456789ABCDEF

test-2: check
	$(RUN) 0x0102040810204080

test-3: check
	$(RUN) 0x53AC691824FEDB70

test-4: check
	$(RUN) 0xF00DCAFEC0DEBEEF

test-random: MAXINSNS=$(shell echo $$(($(ILIMIT)*1000))) 
test-random: check
	$(RUN) -r 1000

test-all: test-1 test-2 test-3 test-4 test-random

test-bonus: CHECK += --min-ipc $(MINIPC)
test-bonus: check

clean:
	rm -f .packages main *.o *.out *~

.PHONY: check clean test-1 test-2 test-3 test-4 test-random test-all

# vim: ts=8 sw=8 noet
