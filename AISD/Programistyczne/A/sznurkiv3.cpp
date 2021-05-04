#include <algorithm>
#include <cmath>
#include <iostream>
#include <utility>

using namespace std;

typedef pair<long long, long long> node_t;
class Heap {
  int size;

public:
  node_t *table;

  Heap(node_t arr[], int n) {
    this->size = n;
    table = arr;
    for (int i = n / 2 - 1; i >= 0; i--)
      trickle_down(i, size);
  }

  void insert(node_t element);
  node_t pop_heap();
  ~Heap() { delete[] table; }
  bool empty() { return size <= 0; }
  node_t top();

private:
  void trickle_down(int pos, int n);
  void trickle_up(int pos);
};

void Heap::insert(node_t element) {
  table[size] = element;
  trickle_up(size);
  size++;
}

node_t Heap::pop_heap() {
  auto value = table[0];
  table[0] = table[size - 1];
  size--;
  trickle_down(0, size);
  return value;
}
long long get_value(node_t element) { return element.first; }
long long get_count(node_t element) { return element.second; }

void Heap::trickle_down(int pos, int n) {

  int smaller = pos, idx = n;

  while (idx != smaller) {
    idx = smaller;
    int chld1 = 2 * idx + 1, chld2 = chld1 + 1;

    if (chld1 < n && get_value(table[smaller]) > get_value(table[chld1]))
      smaller = chld1;

    if (chld2 < n && get_value(table[smaller]) > get_value(table[chld2]))
      smaller = chld2;

    swap(table[idx], table[smaller]);
  }
}

void Heap::trickle_up(int pos) {

  int parent_pos = (pos - 1) / 2;

  while (parent_pos >= 0 &&
         get_value(table[pos]) < get_value(table[parent_pos])) {
    swap(table[pos], table[parent_pos]);
    pos = parent_pos;
    parent_pos = (pos - 1) / 2;
  }
}

node_t Heap::top() { return table[0]; }

int main() {
  ios_base::sync_with_stdio(false);

  int n, result = 0;
  long long nd, d;

  cin >> n;

  auto arr = new node_t[n + 1];

  for (int i = 0; i < n; i++) {
    cin >> d >> nd;
    arr[i] = make_pair(d, nd);
  }

  auto twines = Heap(arr, n);

  while (!twines.empty()) {

    auto k = twines.pop_heap();

    auto elements = get_count(k);
    auto length = get_value(k);

    auto next_element = twines.top();

    while ((get_value(next_element) == length) && !twines.empty()) {

      elements += get_count(next_element);
      (void)twines.pop_heap();
      next_element = twines.top();
    }

    if (elements >= 2) {
      twines.insert(make_pair(length * 2, elements / 2));
      elements %= 2;
    }

    result += elements;
  }

  cout << result;
}
