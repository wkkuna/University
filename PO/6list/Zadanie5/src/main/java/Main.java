//Wiktoria Kuna 316418

import java.util.Arrays;

public class Main {

    static void merge(int arr[], int l, int r) {
        int mid = (l + r) / 2;
        int nl = mid - l + 1;
        int nr = r - mid;

        int L[] = Arrays.copyOfRange(arr, l, mid + 1);
        int R[] = Arrays.copyOfRange(arr, mid + 1, r + 1);

        int lptr = 0, rptr = 0;
        int j = l;

        while (lptr < nl && rptr < nr) {
            if (L[lptr] <= R[rptr])
                arr[j] = L[lptr++];
            else
                arr[j] = R[rptr++];
            j++;
        }

        while (lptr < nl)
            arr[j++] = L[lptr++];

        while (rptr < nr)
            arr[j++] = R[rptr++];

    }

    static void mergesort(int arr[], int l, int r) throws Exception {
        if (l < r) {
            int mid = (l + r) / 2;

            Thread th = new Thread(new Runnable() {
                @Override
                public void run() {
                    try {
                        mergesort(arr, l, mid);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            });

            //Wielowątkowość (rozpoczyna nowy wątek dla pierwszej połowy
            //zaś dla drugiej pozostaje w tym samym)
            th.start();
            mergesort(arr, mid + 1, r);
            th.join();
            merge(arr, l, r);
        }

    }

    static void Mergesort(int arr[]) throws Exception {
        mergesort(arr, 0, arr.length - 1);
    }

    //Przykładowe użycie
    public static void main(String[] argv) {
        int a[] = {4, 2, 0, 8, 9, 4, 8, 0};
        int b[] = {1};
        int c[] = {1, 2 ,3};
        int d[] = {3, 2 ,1};

        try {
            Mergesort(a);
            Mergesort(b);
            Mergesort(c);
            Mergesort(d);
        } catch (Exception e) {
            e.printStackTrace();
        }

        System.out.print("a: ");
        for (var el : a) {
            System.out.print(el + " ");
        }
        System.out.println();

        System.out.print("b: ");
        for (var el : b) {
            System.out.print(el + " ");
        }
        System.out.println();

        System.out.print("c: ");
        for (var el : c) {
            System.out.print(el + " ");
        }
        System.out.println();

        System.out.print("d: ");
        for (var el : d) {
            System.out.print(el + " ");
        }
        System.out.println();
    }
}
