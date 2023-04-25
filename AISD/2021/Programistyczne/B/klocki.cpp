// Wiktoria Kuna 316418

#include <iostream>

using namespace std;

int main() {
  ios_base::sync_with_stdio(false);
  int n;
  cin >> n;
  int h[n], sum = 0;

  for (int i = 0; i < n; i++) {
    cin >> h[i];
    sum += h[i];
  }

  int sub_sums[2][sum + 1];

  for (int i = 0; i <= sum; i++)
    sub_sums[1][i] = -1;
  
  sub_sums[1][0] = 0;

  int prev_row = 0, crr_row = 0, min_diff = sum;

  for (int i = 0; i < n; i++) {
    prev_row = (i+1)%2 , crr_row = 1 - prev_row;

    copy(sub_sums[prev_row], sub_sums[prev_row] + sum + 1, sub_sums[crr_row]);

    int crr_elem = h[i];

    for (int diff = 0; diff <= sum; diff++) {
      int prev_elem = sub_sums[prev_row][diff];
      if (prev_elem == -1)
        continue;

      int sum2 = prev_elem + crr_elem;
      int d1 = abs(diff - crr_elem), d2 = diff + crr_elem;

      if (i > 0)
        min_diff = min(d1, min_diff);

      sub_sums[crr_row][d1] = max(sub_sums[crr_row][d1], sum2);
      sub_sums[crr_row][d2] = max(sub_sums[crr_row][d2], sum2);
    }
  }

  if (sub_sums[crr_row][0] > 0)
    cout << "TAK\n" << sub_sums[crr_row][0] / 2 << "\n";
  else
    cout << "NIE\n" << min_diff << "\n";
}
