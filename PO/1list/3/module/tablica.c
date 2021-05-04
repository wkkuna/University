//Wiktoria Kuna 316418
#include "tablica.h"

array *initialize_array()
{
    return NULL;
}

array *place_elements_head(array *t, Tkey key)
{
    for (int i = t->key - 1; i > key; i--)
    {
        array *newnode = malloc(sizeof(array));
        newnode->value = 0;
        newnode->key = i;
        newnode->next = t;
        t = newnode;
    }
    return t;
}

array *place_elements_tail(array *t, Tval value, Tkey key)
{
    array *temp = t;

    while (temp->next != NULL)
        temp = temp->next;

    for (int i = t->key + 1; i < key; i++)
    {
        array *newnode = malloc(sizeof(array));
        newnode->value = 0;
        newnode->key = i;
        newnode->next = NULL;
        temp->next = newnode;

        temp = temp->next;
    }

    array *newnode = malloc(sizeof(array));
    newnode->key = key;
    newnode->value = value;
    newnode->next = NULL;
    temp->next = newnode;

    return t;
}

array *find_ptr(array *t, Tkey key)
{
    if (t == NULL)
        return t;

    array *temp = t;

    while (temp->next != NULL)
    {
        if (temp->key == key)
            return temp;
        temp = temp->next;
    }

    if(temp->key == key)
        return temp;

    return NULL;
}

Tval idx(array *t, Tkey key)
{
    if (t == NULL)
    {
        printf("Empty array\n");
        return 0;
    }

    array *temp = find_ptr(t, key);

    if(temp != NULL)
        return temp->value;

    printf("No element with given index: %d\n", key);
    return 0;
}

array *add(array *t, Tval value, Tkey key)
{
    array *newnode = malloc(sizeof(array));
    newnode->key = key;
    newnode->value = value;
    newnode->next = NULL;

    if (t == NULL)
        return newnode;

    if (t->key > key)
    {
        newnode->next = place_elements_head(t, key);
        return newnode;
    }

    free(newnode);

    array *temp = find_ptr(t, key);

    if (temp != NULL)
        temp->value = value;

    else if (temp == NULL)
        t = place_elements_tail(t, value, key);

    return t;
}

void print_array(array *t)
{
    array *temp = t;
    while (temp != NULL)
    {
        printf("[%d] %d\n", temp->key, temp->value);
        temp = temp->next;
    }
}

void free_array(array* head)
{
   array* tmp;

   while (head != NULL)
    {
       tmp = head;
       head = head->next;
       free(tmp);
    }

}
