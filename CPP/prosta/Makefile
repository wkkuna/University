CC = g++

CCFLAG = -Wall -Wextra -pedantic -std=c++17 -Wfloat-equal -Winit-self -g3 -o0
SANITIZE = -Wuninitialized -fsanitize=leak -fno-common -fno-omit-frame-pointer -fsanitize=address -fsanitize=undefined -fstack-protector-all

BUILD = build/
OBJ = $(BUILD)obj/

all: prosta demo

prosta: 
	$(CC) $(CCFLAG) $(SANITIZE) -o $(OBJ)prosta.o -c prosta.cpp
demo: 
	$(CC) $(CCFLAG) -Wall -c demo_prosta.cpp -o $(OBJ)demo_prosta.o
	$(CC) $(CCFLAG) $(SANITIZE) $(OBJ)prosta.o $(OBJ)demo_prosta.o -o $(BUILD)demo_prosta
clean:
	rm $(obj)prosta.o $(obj)demo_prosta.o $(build)demo_prosta
