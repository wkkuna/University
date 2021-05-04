//Wiktoria Kuna 316418
#include "stos.hpp"

void stack::insert(string x)
{
    if(noe == capacity)
       throw invalid_argument("Stack overflow");

    stackPtr[noe] = x;
    noe++;
}

string stack::pop()
{
    if(noe == 0)
        throw invalid_argument("Stack is empty");
    
    return stackPtr[--noe];
}

string stack::peekTop()
{
    if(noe == 0)
        throw invalid_argument("Stack is empty");
    
    return stackPtr[noe-1];
}

int stack::size()
{
    return noe;
}

void stack::printStack()
{
    for(int i=0; i< noe; i++)
        cout << stackPtr[i]<< endl;
}
