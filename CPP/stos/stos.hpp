//Wiktoria Kuna 316418
#ifndef STACK

#define STACK
#include <iostream>
#include <vector>
using namespace std;

class stack
{
    private:
    string *stackPtr;
    int capacity;
    int noe;

    public:
    void insert(string x);
    string pop();
    string peekTop();
    int size();
    void printStack();
    
    stack(int x)
    {
        if(x < 0 || x > 100)
            throw invalid_argument("Invalid stack size");

        capacity = x;
        stackPtr = new string[x];
    }
    stack() : stack(1){};

    stack(initializer_list<string> x) : stack(x.size())
    {
        for (const auto &elem: x)
            this->insert(elem);
    }

    stack(const stack& stc) :stack(stc.capacity)
    {
        for(int i=0; i < stc.noe; i++)
            this->insert(stc.stackPtr[i]);
    }
    
    stack(stack&& stc) : capacity(stc.capacity), noe(stc.noe), stackPtr(stc.stackPtr)   
    {
        stc.stackPtr = nullptr;
    }
};

#endif