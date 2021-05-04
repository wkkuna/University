//Wiktoria Kuna 316418
//   ##########################################################
//   #             **Następnym razem**                        #
//   # Warto zwórcić uwagę na typy wykonując działania.       #
//   # W programie pojawia się często one << idx zamiast      #
//   # 1 << idx. Jest tak dlatego, że idx jest typu int       #
//   # (32-bitowy). Dlatego chcąc przypisać wyrażenie do      #
//   # zmiennej typu uint64_t działanie 1 << idx potraktuje   #
//   # jako działanie na int i dopiero potem dokona konwersji #
//   # na uint64_t, co nie da nam oczekiwanych rezultatów...  #
//   # Stąd potrzebna jest zmienna typu uint64_t, wtedy       #
//   # wyrażenie wykona się na w/w typie lub bezpośrednia     #
//   # konwersja idx na uint64_t.                             #
//   ###########################################################

#include "tabbit.hpp"

//                             **ref CONSTRUCTOR**

tab_bit::ref::ref(tab_bit *w, int i)
{
    if (w == nullptr)
        throw invalid_argument("Referencja do pustej tab_bit");

    if (i < 0 || i >= w->dl)
        throw invalid_argument("Przekroczenie zakresu tab_bit");

    uint64_t one = 1;

    s = &(w->tab)[i / rozmiarSlowa];  //słowo, które zawiera dany indeks w tablicy tab
    idx = i % rozmiarSlowa;           //ideks bitu w wyodrębnionym słowie
    val = (*s & (one << idx)) >> idx; //wartość bitu (1 lub 0)
}

//                          **ref OPERATORS OVERLOADS**

tab_bit::ref::operator bool()
{
    return val;
}

tab_bit::ref &tab_bit::ref::operator=(const ref x)
{
    return this->operator=(x.val);
}

tab_bit::ref &tab_bit::ref::operator=(bool val)
{
    uint64_t one = 1;
    uint64_t mask = ~(one << idx);
    uint64_t tmp = *(this->s) & mask;        //zgaszenie bitu na pozycji idx
    *(this->s) = tmp | (uint64_t)val << idx; //zapalenie biu, jeśli val jest 1
    s = this->s;
    this->val = val;

    return *this;
}

tab_bit::ref tab_bit::operator[](int i)
{
    return ref(this, i);
}

//                        **tab_bit OPERATOR OVERLOADS**

tab_bit &tab_bit::operator=(const tab_bit &tb)
{
    dl = tb.dl;
    delete[] tab;

    int s = dl / rozmiarSlowa;
    tab = new slowo[s + 1];

    for (int i = 0; i <= s; i++)
        tab[i] = (tb.tab)[i];

    return *this;
}

tab_bit &tab_bit::operator=(tab_bit &&tb)
{
    dl = tb.dl;
    delete[] tab;
    tab = tb.tab;
    tb.tab = nullptr;

    return *this;
}

bool tab_bit::operator[](int i) const
{
    if (i < 0 || i >= this->dl)
        throw invalid_argument("Przekroczenie zakresu tab_bit");

    int idx = dl - 1 - i;
    uint64_t one = 1;

    slowo *_s = &(this->tab)[idx / rozmiarSlowa];
    idx = idx % rozmiarSlowa;

    return ((*_s & (one << idx)) >> idx);
}

ostream &operator<<(ostream &wy, const tab_bit &tb)
{
    for (int i = 0; i < tb.dl; i++)
        wy << tb[i];

    return wy;
}

istream &operator>>(istream &we, tab_bit &tb)
{
    string str;

    if (we >> str)
    {
        int size = str.size() - 1;

        if (tb.dl <= size)
            throw invalid_argument("Nieodpowiednia długość tab_bit");

        for (int i = 0; i <= size; i++)
        {
            if (str[size - i] != '1' && str[size - i] != '0')
                throw invalid_argument("Nieodpowienie wartości dla tab_bit");

            tb[i] = (str[size - i] - '0');
        }
    }

    return we;
}

//                   **tab_bit CONSTRUCTORS & DESTRUCTOR**

tab_bit::tab_bit(initializer_list<bool> xs) : tab_bit((int)xs.size())
{
    int i = dl - 1;

    for (auto x : xs)
    {
        this->operator[](i) = x; //przypisuje odpowiednią wartoś
                                 //do i-tego bitu
        i--;
    }
}

tab_bit::tab_bit(int rozm)
{
    dl = rozm;
    int s = rozm/rozmiarSlowa ; //ilość potrzebnych do
                                       //zaalokowania miejsc
                                       //w tab - 1

    tab = new slowo[s+1]; //alokacja

    for (int i = 0; i <= s; i++)
        tab[i] = 0;
}

tab_bit::tab_bit(slowo tb)
{
    dl = rozmiarSlowa;
    tab = new slowo[1];
    tab[0] = tb;
}

tab_bit::tab_bit(const tab_bit &tb)
{
    dl = tb.dl;
    int s = dl / rozmiarSlowa;
    tab = new slowo[s + 1];

    for (int i = 0; i <= s; i++)
        tab[i] = (tb.tab)[i];
}

tab_bit::tab_bit(tab_bit &&tb)
{
    dl = tb.dl;
    tab = tb.tab;

    tb.tab = nullptr;
}

tab_bit::~tab_bit()
{
    delete[] tab;
}

//                    **tab_bit BITWISE OPERATIONS**

tab_bit tab_bit::operator|(const tab_bit &T)
{
    if (T.dl > this->dl)
    {
        tab_bit tmp(T);
        tmp |= *this;
        return tmp;
    }

    tab_bit tmp(*this);
    tmp |= T;
    return tmp;
}

tab_bit tab_bit::operator|=(const tab_bit &T)
{
    int sl_a = this->dl / rozmiarSlowa;
    int sl_b = T.dl / rozmiarSlowa;
    int diff = sl_b - sl_a;

    for (int i = sl_a; i >= 0; i--)
    {
        if (i + diff < 0)
            break;

        this->tab[i] |= T.tab[i + diff];
    }

    return *this;
}

tab_bit tab_bit::operator&(const tab_bit &T)
{
    if (T.dl > this->dl)
    {
        tab_bit tmp(T);
        tmp &= *this;
        return tmp;
    }

    tab_bit tmp(*this);
    tmp &= T;
    return tmp;
}

tab_bit tab_bit::operator&=(const tab_bit &T)
{
    int sl_a = this->dl / rozmiarSlowa;
    int sl_b = T.dl / rozmiarSlowa;
    int diff = sl_b - sl_a;

    for (int i = sl_a; i >= 0; i--)
    {
        if (i + diff < 0)
            break;

        this->tab[i] &= T.tab[i + diff];
    }

    for (int i = 0; i < -diff; i++)
        this->tab[i] = 0;

    return *this;
}

tab_bit tab_bit::operator^(const tab_bit &T)
{
    if (T.dl > this->dl)
    {
        tab_bit tmp(T);
        tmp ^= *this;
        return tmp;
    }

    tab_bit tmp(*this);
    tmp ^= T;
    return tmp;
}

tab_bit tab_bit::operator^=(const tab_bit &T)
{
    int sl_a = this->dl / rozmiarSlowa;
    int sl_b = T.dl / rozmiarSlowa;
    int diff = sl_b - sl_a;

    for (int i = sl_a; i >= 0; i--)
    {
        if (i + diff < 0)
            break;

        this->tab[i] ^= T.tab[i + diff];
    }

    return *this;
}

bool tab_bit::operator!()
{
    bool flag = 1;

    for (int i = this->dl / rozmiarSlowa; i >= 0; i--)
    {
        if (this->tab[i] != 0)
        {
            flag = 0;
            break;
        }
    }
    return flag;
}

//                    **tab_bit OTHER METHODS**
int tab_bit::rozmiar() const
{
    return dl;
}
