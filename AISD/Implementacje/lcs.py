def lcs(x: str, y: str):
    xarr, yarr = list(x), list(y)
    h, w = len(yarr), len(xarr)
    lcs_arr = [[0] * (w + 1) for _ in range(h + 1)]

    for i in range(0, h + 1):
        for j in range(0, w + 1):
            if j == 0 or i == 0:
                lcs_arr[i][j] = 0
            elif xarr[j - 1] == yarr[i - 1]:
                lcs_arr[i][j] = lcs_arr[i-1][j-1] + 1
            else:
                lcs_arr[i][j] = max(lcs_arr[i-1][j], lcs_arr[i][j-1])

    # Reconstruct the LCS
    lcs_len = lcs_arr[h][w]
    lcs = ''
    i, j = h, w

    while lcs_len > 0:
        if xarr[j - 1] == yarr[i - 1]:
            lcs += xarr[j - 1]
            i -= 1
            j -= 1
            lcs_len -= 1
        elif lcs_arr[i - 1][j] > lcs_arr[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return lcs[::-1]
