CC = g++

CCFLAG = -Wall -Wextra -pedantic -std=c++17 -Wfloat-equal -Winit-self -g3 -o0
SANITIZE = -Wuninitialized -fsanitize=leak -fno-common -fno-omit-frame-pointer -fsanitize=address -fsanitize=undefined -fstack-protector-all
SLG = -lgsl -lgslcblas -lm

all: clean ex1

ex1: 
	$(CC) $(CCFLAG) $(SANITIZE) -o ex1 ex1.cpp
clean:
	rm -f ex1;