#include <iostream>
using namespace std;

#define N 5
#define F 3

int main() {
  int n, p, m;

  cin >> n >> p >> m;

  bool forbbiden_pattern[3][3] = {0};
  char symbol;

  for (int i = 0; i < p; p++) {
    for (int j = 0; j < F; j++) {
      for (int k = 0; k < F; k++) {
        cin >> symbol;
        if (symbol == '.')
          forbbiden_pattern[j][k] = 0;
        else
          forbbiden_pattern[j][k] = 1;
      }
    }
    
  }



}