PROGS = shell

include Makefile.include

# If you're getting SIGSEGV uncomment following line on your local computer.
# WARNING: This must not be enabled on GitHub Classroom !
# CC += -fsanitize=address
LDLIBS += -lreadline

all: shell trace.so

shell: shell.o command.o lexer.o jobs.o

test:
	python3 sh-tests.py -v

trace.so: trace.c
	gcc -Wall -O2 -shared -fpic -o trace.so trace.c -ldl

# vim: ts=8 sw=8 noet
