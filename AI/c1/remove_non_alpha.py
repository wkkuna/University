with open("pantadeusz.txt") as f, open("pantadeusz_spacje.txt", 'w') as out, open("pantadeusz_bez_spacji.txt", 'w') as out2:
    text = f.readline()
    while text:
        if text == "\n":
            text = f.readline()
            continue
        output = ''.join(filter(lambda x: x.isalpha() or x == ' ', text)) + "\n"
        output = output.lower()
        text = f.readline()
        out.write(output)
        out2.write(output.replace(" ", ""))