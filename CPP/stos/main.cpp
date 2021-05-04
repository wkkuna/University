//Wiktoria Kuna 316418
#include "stos.hpp"

vector<pair<string, int>> cmd =
    {
        {"stackA", 1},
        {"stackB", 2},
        {"stackRmv", 3},
        {"ins", 4},
        {"pop", 5},
        {"peek", 6},
        {"size", 7},
        {"prt", 8},
        {"exit", 9}};

int main(int argc, char *argv[])
{
    auto A = new stack({"A", "B", "C"});
    auto B = new stack({"C", "B", "A"});

    // A->printStack();
    // B->printStack();

    //Używanie konstruktora kopiującego
    auto C = B;
    //Używanie konstruktora przenoszącego
    auto D = move(A);
    
    delete(D);
    delete(C);
    // C->printStack();
    // D->printStack();

    cout << "Type:" << endl;
    cout << "To create a stack:" << endl;
    cout << "stackA (deafult size: 1)" << endl;
    cout << "stackB <size of stack>" << endl
         << endl;

    cout << "stackRmv - to remove current stack" << endl
         << endl;

    cout << "ins <string> - push on stack" << endl;
    cout << "pop - pop off stack" << endl;
    cout << "peek - peek recently laid element" << endl;
    cout << "size - number of elements on current stack" << endl;
    cout << "prt - print current stack" << endl;
    cout << "exit - to exit program" << endl
         << endl;

    string command, argStr;
    stack *S = nullptr;
    int arg;

    try
    {
        while (true)
        {
            int cmdId = 0;
            cin >> command;

            for (auto &p : cmd)
                if (command == p.first)
                    cmdId = p.second;

            switch (cmdId)
            {
            case 0:
                cout << "unkown command\n";
                break;

            case 1:
                S = new stack();
                break;

            case 2:
                cin >> arg;
                S = new stack(arg);
                break;

            case 3:
                delete (S);
                break;

            case 4:
                if (S == nullptr)
                    throw invalid_argument("Stack not initialized");
                cin >> argStr;
                S->insert(argStr);
                break;

            case 5:
                if (S == nullptr)
                    throw invalid_argument("Stack not initialized");
                cout << S->pop() << endl;
                break;

            case 6:
                if (S == nullptr)
                    throw invalid_argument("Stack not initialized");
                cout << S->peekTop() << endl;
                break;

            case 7:
                cout << S->size() << endl;
                break;

            case 8:
                S->printStack();
                break;

            case 9:
                delete (S);
                exit(0);
                break;

            default:
                break;
            }
        }
    }
    catch (const exception &e)
    {
        cerr << e.what() << '\n';
    }
}