CC = gcc

CCFLAG = -Wall -Wextra -pedantic -std=c11 -Wfloat-equal -Winit-self -g3 -o0
SANITIZE = -Wuninitialized -fsanitize=leak -fno-common -fno-omit-frame-pointer -fsanitize=address -fsanitize=undefined -fstack-protector-all
SLG = -lgsl -lgslcblas -lm

BUILD = build/
MODULE = module/
OBJ = $(BUILD)obj/

all: tablica

tablica: 
	$(CC) $(CCFLAG) $(SANITIZE) -o $(OBJ)tablica.o -c $(MODULE)tablica.c
demo: 
	$(CC) -Wall -c demo_tablica.c -o $(OBJ)demo_tablica.o
	$(CC) $(CCFLAG) $(SANITIZE) $(OBJ)tablica.o $(OBJ)demo_tablica.o $(SLG) -o $(BUILD)demo_tablica
clean:
	rm build/* 
	build/obj/*