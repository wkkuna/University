// Wiktoria Kuna 316418
#ifndef LINKED_LIST
#define LINKED_LIST 
#include<bits/stdc++.h>

template<typename T>
class List{
private:
    class Node{
    public:
        int key;
        T value;
        Node* next;

    public:
        Node(int, T);
    };
    uint noe = 0;
    Node* node = nullptr;    

public:
    //Places an element at given key replaces 
    //it with new value if it already exists
    void insert(int key, T value);
    
    // Removes an element of given value with the smallest key
    // (since it wasn't specified by the task) 
    // if element is not on a list - does nothing
    void remove(T value);

    // if an element is on the list
    // returns the key; -1 otherwise
    int search(T value);
    uint size();

    List();
    List(std::initializer_list<T>);
    List(List&);
    List(List&&);

    List& operator=(const List&);
    List& operator=(const List&&);

    template<typename U>
    friend std::ostream& operator<<(std::ostream& os, const List<U>&);

    ~List();
};


/**********************************************
           CONSTRUCTORS
**********************************************/

/********** NODE **********/
template<typename T>
List<T>::Node::Node(int key, T value) : key(key), value(value), next(nullptr){}

/********** LIST **********/

template<typename T>
List<T>::List() : noe(0), node(nullptr){}

template<typename T>
List<T>::List(List& old)
{
    noe = old.noe;
    node = new Node(old.node->key,old.node->value);

    auto *tmp = old.node->next; 
    auto *iter = node;
    while(tmp!=nullptr)
    {
        iter->next = new Node(tmp->key,tmp->value);
        iter = iter->next;
        tmp = tmp->next;
    }
    iter->next = nullptr;
}

template<typename T>
List<T>::List(List&& old)
{
    noe = old.noe;
    node = old.node;
    old.node = nullptr;
}

template<typename T>
List<T>::List(std::initializer_list<T> x)
{
    int i = 0;
    for(auto e : x){
        insert(i,e);
    }
    noe = i;
}

/**********************************************
             ASSIGMENTS
**********************************************/

template<typename T>
List<T>& List<T>::operator=(const List<T>& x)
{
    if(&x == this)
        return *this;

    if(node == nullptr)
    {
        noe = x.noe;
        node = x.node;
    }
    else
    {
        delete(node);
        noe = x.noe;
        this = new List<T>(x);
    }

    return *this;
}

template<typename T>
List<T>& List<T>::operator=(const List<T>&& x)
{
    if(&x == this)
        return *this;

    if(node!=nullptr)
        delete(node);

    node = x.node;
    noe = x.noe;

    x.node = nullptr;
    x.noe = 0;

    return *this;
}


/**********************************************
            LIST OPERATIONS
**********************************************/

template<typename T>
uint List<T>::size() {return noe;}

template<typename T>
void List<T>::insert(int key, T value)
{
    // empty list case
    if(node == nullptr)
    {
        node = new Node(key, value);
        noe++;
        return;
    }

    // place at the begining
    if(node->key > key)
    {
        auto *tmp = node;
        node = new Node(key, value);
        node->next = tmp;
        noe++;
        return;
    }

    auto *iter = node;
    // place in the middle
    while(iter!=nullptr && iter->next != nullptr)
    {   
        if(iter->key == key)
        {
            iter->value = value;
            return;
        }

        if(iter->next->key > key)
        {
            auto *tmp = iter->next;
            iter->next = new Node(key, value);
            iter->next->next = tmp;
            noe++;
            return;
        }

        iter = iter->next;
    }

    // place at the end
    if(iter->key < key)
    {
        iter->next = new Node(key, value);
        noe++;
    }

    else if(iter->key == key)
        iter->value = value;
}

template<typename T>
void List<T>::remove(T value)
{
    // empty list
    if(node == nullptr)
        throw "Attempted to remove an element from an empty list";

    // element at the begining
    if(node->value == value)
    {
        auto *tmp = node->next;
        delete(node);
        node = tmp;
        noe--;
        return;
    }

    auto *iter = node;

    //element in the middle
    while (iter!=nullptr && iter->next!=nullptr)
    {
        if(value == iter->next->value)
        {
            auto *tmp = iter->next->next;
            delete(iter->next);
            iter->next = tmp;
            noe--;
            return;
        }
        iter = iter->next;
    }
    
    // //element at the end
    // if(iter->next->value == value)
    // {
    //     delete(iter->next);
    //     iter->next = nullptr;
    //     noe--;
    // }
}

template<typename T>
int List<T>::search(T value)
{
    auto *iter = node;

    while(iter!=nullptr)
    {
        if(iter->value == value)
            return iter->key;
        iter = iter->next;
    }
    return -1;
}

/**********************************************
                DESTRUCTORS
**********************************************/

// -fsanitize=address -fno-omit-frame-pointer
template<typename T>
List<T>::~List()
{
   Node* currentNode = node; 
    while (currentNode)
    {
        Node* nextNode = currentNode->next;    
        delete(currentNode);                        
        currentNode = nextNode;                 
    }
}

template<typename T>
std::ostream& operator<<(std::ostream& out, const List<T>& list)
{
    auto *tmp = list.node;
    while (tmp!=nullptr)
    {
        out << "(" + std::to_string(tmp->key) + ", " + std::to_string(tmp->value) + ")\n";
        tmp = tmp->next;
    }
    return out;
}

#endif