// Wiktoria Kuna 316418

#include <algorithm>
#include <cmath>
#include <iostream>

using namespace std;

pair<long long, long long> *arr;

pair<int, int> binsearch(int beg, int end, long long elem_val) {
  int mid = 0;
  while (end >= beg) {
    mid = (end + beg) / 2;
    long long mid_val = arr[mid].first;

    if (elem_val == mid_val)
      return make_pair(1, mid);
    else if (elem_val > mid_val)
      beg = mid + 1;
    else
      end = mid - 1;
  }

  return make_pair(0, mid);
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
    long long elements = arr[i].second;

    if (elements < 2) {
      result += elements;
      continue;
    }

    pair<int, int> idx;
    int boundry = i;

    for (long long j = arr[i].first; elements > 0; j *= 2) {
      result += elements % 2;
      elements /= 2;

      if ((idx = binsearch(boundry, n, 2 * j)).first) {
        auto pos = idx.second;
        elements += arr[pos].second;
        arr[pos].second = 0;
      }

      boundry = idx.second;
    }
  }

  printf("%d", result);
}