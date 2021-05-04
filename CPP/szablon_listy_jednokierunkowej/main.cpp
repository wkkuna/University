// Wiktoria Kuna 316418
#include "single_linked_list.hpp"

int main()
{
    List<int> xs = List<int>();
    xs.insert(0, 0);
    std::cout << "List:\n" << xs;
    std::cout << "Number of elements: " << xs.size() << std::endl;
    xs.insert(1,1);
    std::cout << "List:\n" << xs;
    std::cout << "Number of elements: " << xs.size() << std::endl;
    xs.insert(10,10);
    std::cout << "List:\n" << xs;
    std::cout << "Number of elements: " << xs.size() << std::endl;
    xs.insert(2,2);
    std::cout << "List:\n" << xs;
    std::cout << "Number of elements: " << xs.size() << std::endl;
    xs.insert(-5,12);
    std::cout << "List:\n" << xs;
    std::cout << "Number of elements: " << xs.size() << std::endl;
    xs.remove(1);
    std::cout << "List:\n" << xs;
    std::cout << "Number of elements: " << xs.size() << std::endl;
    xs.remove(12);
    std::cout << "List:\n" << xs;
    std::cout << "Number of elements: " << xs.size() << std::endl;
    xs.insert(-3,3);
    std::cout << "List:\n" << xs;
    std::cout << "Number of elements: " << xs.size() << std::endl;
    xs.remove(10);
    std::cout << "List:\n" << xs;
    std::cout << "Number of elements: " << xs.size() << std::endl;
    xs.insert(15,3);


    std::cout << "List:\n" << xs;
    std::cout << "Number of elements: " << xs.size() << std::endl;

    if(xs.search(3))
        std::cout<< "I found 3 on your list! - enough to pass C:\n";
    if(xs.search(42) == -1)
        std::cout<< "I have not found 42 on your list! - no answer to all questions today :c\n";

    auto xss = xs;

    std::cout << "copying:\n" << xss << "\n";

    auto xsss = std::move(xss);
    
    std::cout <<"moving:\n" << xsss;
    std::cout <<"old one:\n" << xss;
    std::cout << "IT'S A MOVE - no old one.\n";
}