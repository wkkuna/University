def common_prefix(string_list):
    def common_prefix_three(s1, s2, s3):
        prefix = ""
        for x, y, z in zip(s1, s2, s3):
            if x == y and y == z:
                prefix += x
            else:
                return prefix

    if len(string_list) < 3:
        return ""

    string_list = list(map(lambda x: x.lower(), string_list))
    string_list.sort()

    longest_prefix = ""
    for idx in range(0, len(string_list)-2):
        prefix = common_prefix_three(
            string_list[idx], string_list[idx+1], string_list[idx+2])
        if len(prefix) > len(longest_prefix):
            longest_prefix = prefix

    return longest_prefix


print(common_prefix(["Cyprian", "cyberotoman", "cynik", "ceniąc", "czule"]))
print(common_prefix(["Cyprian", "bankomant",
      "cynik", "bank", "bicz", "bańki"]))
