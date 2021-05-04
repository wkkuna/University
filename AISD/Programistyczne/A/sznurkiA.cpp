#include <algorithm>
#include <assert.h>
#include <cmath>
#include <iostream>
#include <list>

using namespace std;

list<pair<long long, long long>> twines = {};

int main() {
  long long n, nd, d, result = 0;

  assert(scanf("%lld", &n) == 1);

  for (long long i = 0; i < n; i++) {
    assert(scanf("%lld %lld", &d, &nd) == 2);
    twines.emplace_back(nd, d);
  }

  twines.sort([](pair<long long, long long> a, pair<long long, long long> b) {
    return a.second < b.second;
  });
  

  while (!twines.empty()) {
    auto k = twines.begin();

    auto elements = k->second;

    if (elements >= 2) {

      auto value = k->first * 2;
      auto e = elements / 2;

      twines[value] += e;
      elements %= 2;
    }

    if (elements == 1)
      result++;
    twines.erase(k);
  }
  printf("%lld\n", result);
}
