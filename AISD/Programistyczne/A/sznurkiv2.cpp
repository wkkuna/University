#include <algorithm>
#include <assert.h>
#include <cmath>
#include <iostream>
#include <utility>
#include <vector>

using namespace std;

typedef pair<long long, long long> node_t;
class Heap {
  node_t *table;
  int size;

  Heap(int n) {
    table = new node_t[n];
    size = n;
  }

  ~Heap() { delete (table); }

  void insert(node_t element);
  node_t pop_heap();
  void trickle_down(int pos);
  void trickle_up(int pos);
  void trickle(int pos, node_t elem);

  long long get_value(node_t element);
  long long get_count(node_t element);
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
  trickle_down(0);
  return value;
}

void Heap::trickle_down(int pos) {
  int chld_pos1 = 2 * pos - 1, chld_pos2 = chld_pos1 + 1;
  auto chld1 = table[chld_pos1], chld2 = table[chld_pos2];

  if (pos >= size)
    return;

  if (table[pos] > min(chld2, chld2)) {
    if (chld2 > chld1) {
      swap(table[pos], table[chld_pos2]);
      trickle_down(chld_pos2);
    } else {
      swap(table[pos], table[chld_pos1]);
      trickle_down(chld_pos1);
    }
  }
}

void Heap::trickle_up(int pos) {
  int parent_pos = pos / 2 - 1;

  if (parent_pos >= 0 && table[pos] < table[parent_pos]) {
    swap(table[pos], table[parent_pos]);
    trickle_up(parent_pos);
  }
}

long long Heap::get_value(node_t element) { return element.first; }
long long Heap::get_count(node_t element) { return element.second; }

// Długość sznurka; liczba sznurków
auto twines = vector<pair<long long, long long>>();

int main() {
  int n;
  long long nd, d, result = 0;
  assert(scanf("%d", &n) == 1);

  for (int i = 0; i < n; i++) {
    assert(scanf("%lld %lld", &d, &nd) == 2);
    twines.push_back(make_pair(d, nd));
  }

  sort(twines.begin(), twines.end(),
       [](pair<long long, long long> a, pair<long long, long long> b) {
         return a.first > b.first;
       });

  while (!twines.empty()) {
    auto k = twines.end() - 1;

    auto elements = k->second;

    if (elements >= 2) {

      auto value = k->first * 2;
      auto e = elements / 2;

      auto j = lower_bound(twines.begin(), twines.end(), value,
                           [value](pair<long long, long long> x,
                                   long long val) { return x.first > val; });

      if (j->first == value)
        j->second += e;
      else
        twines.insert(j, make_pair(value, e));

      elements %= 2;
    }

    if (elements == 1)
      result++;
    twines.pop_back();
  }
  printf("%lld\n", result);
}
