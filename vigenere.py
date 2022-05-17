#!/usr/bin/env python

def encrypt(text: str, key: str) -> str:
    out = ""

    for i in range(len(text)):

        if not text[i].isalpha():
            out += text[i]
            continue

        letter = (ord(text[i]) - ord("a")) % 32

        keyLetter = (ord(key[i % len(key)]) - ord("a")) % 32

        out += chr((letter + keyLetter) % 26 + (ord("a") if text[i].islower() else ord("A")))

    return out

def decrypt(text: str, key: str) -> str:
    out = ""

    for i in range(len(text)):

        if not text[i].isalpha():
            out += text[i]
            continue

        letter = (ord(text[i]) - ord("a")) % 32

        keyLetter = (ord(key[i % len(key)]) - ord("a")) % 32

        out += chr((26 + letter - keyLetter) % 26 + (ord("a") if text[i].islower() else ord("A")))

    return out

if __name__ == "__main__":
    import sys, getopt

    usageString = f"Usage: {sys.argv[0]} [--encrypt] [--decrypt] [-edh] [-k] <key> [[-t] <text>]"

    key = ""
    text = ""
    process = encrypt

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hk:t:de", ["key=", "decrypt", "encrypt", "text="])
    except getopt.GetoptError as msg:
        print(msg, file=sys.stderr)
        print(usageString, file=sys.stderr)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print(usageString)
            sys.exit()
        elif opt in ("-k", "--key"):
            key = arg
        elif opt in ("-d", "--decrypt"):
            process = decrypt
        elif opt in ("-e", "--encrypt"):
            process = encrypt
        elif opt in ("-t", "--text"):
            text = arg

    if key == "":
        if len(args) == 0:
            print("Cipher requires a key", file=sys.stderr)
            print(usageString, file=sys.stderr)
            sys.exit(2)
        else:
            key = args[0]

    if text == "" and len(args) > 1:
        text = args[1]

    if text in ("", "-", "--"):
        while True:
            try:
                print(process(input(), key))
            except EOFError:
                break
    else:
        print(process(text, key))
