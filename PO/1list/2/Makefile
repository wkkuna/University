CC = gcc

CCFLAG = -Wall -Wextra -pedantic -std=c11 -Wfloat-equal -Winit-self -g3 -o0
SANITIZE = -Wuninitialized -fsanitize=leak -fno-common -fno-omit-frame-pointer -fsanitize=address -fsanitize=undefined -fstack-protector-all
SLG = -lgsl -lgslcblas -lm

BUILD = build/
MODULE = module/
OBJ = $(BUILD)obj/

all: clean demo

ulamki: 
	$(CC) $(CCFLAG) $(SANITIZE) -o $(OBJ)ulamki.o -c $(MODULE)ulamki.c
demo: 
	$(CC) -Wall -c ulamki_demo.c -o $(OBJ)ulamki_demo.o
	$(CC) $(CCFLAG) $(SANITIZE) $(OBJ)ulamki.o $(OBJ)ulamki_demo.o $(SLG) -o $(BUILD)ulamki_demo
clean:
	rm build/* 
	build/obj/*