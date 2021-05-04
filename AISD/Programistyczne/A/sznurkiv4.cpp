// Wiktoria Kuna 316418

#include <algorithm>
#include <cmath>
#include <iostream>

using namespace std;

typedef pair<long long, long long> node_t;
inline long long get_value(node_t element) { return element.first; }
inline long long get_count(node_t element) { return element.second; }

pair<long long, long long> *arr;

int binsearch(int beg, int end, long long elem_val) {
  int mid = (beg + end) / 2;

  long long mid_val = get_value(arr[mid]);

  if (elem_val == mid_val)
    return mid;
  if (beg == end)
    return -1;
  if (elem_val < mid_val)
    return binsearch(beg, mid, elem_val);
  else
    return binsearch(mid + 1, end, elem_val);

  return -1;
}

int main() {
  ios_base::sync_with_stdio(false);

  int n, result = 0;
  long long nd, d;

  cin >> n;

  arr = new pair<long long, long long>[n + 1];

  for (int i = 0; i < n; i++) {
    cin >> d >> nd;
    arr[i] = make_pair(d, nd);
  }

  sort(arr, arr + n,
       [](pair<long long, long long> a, pair<long long, long long> b) {
         return a.first < b.first;
       });

  for (int i = 0; i < n; i++) {
    auto k = arr[i];

    auto elements = get_count(k);
    auto length = get_value(k);

    int idx = -1;

    while ((idx = binsearch(i, n, 2 * length)) == -1 && elements > 0) {
      result += elements % 2;
      elements /= 2;
      length *= 2;
    }

    arr[idx].second += elements / 2;
    elements %= 2;
    result += elements;
  }

  printf("%d", result);
}