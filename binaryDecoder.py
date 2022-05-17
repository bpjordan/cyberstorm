#!/usr/bin/env python

###############################################
# Name: Bronson Jordan
# Team: Thoth
# binaryDecoder.py
# Decodes and outputs a string of text encoded
#   as binary 1s and 0s
###############################################

def binaryDecode(text, wordLength, printBS = False):

    out = ""

    while(len(text) >= wordLength):

        val = 0

        word=text[:wordLength]
        text=text[wordLength:]

        for i in range(wordLength):
            val += int(word[-(i+1)]) * pow(2, i)

        if val == 8 and not printBS:
            out = out[:-1]
        else:
            out += chr(val)

    return out

def main():

    import sys, getopt

    usageString = f"Usage: {sys.argv[0]} [-b] [[-t] <encodedString>]"

    encodedString = ""
    printBS = False

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hb", ["encodedString="])
    except getopt.GetoptError as msg:
        print(msg, file=sys.stderr)
        print(usageString, file=sys.stderr)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print(usageString)
            sys.exit()
        elif opt == "-b":
            printBS = True
        elif opt in ("-t", "--encodedString"):
            encodedString = arg


    if len(args) > 0 and encodedString == "":
        encodedString = args[0]

    if encodedString in ("", "-", "--"):
        encodedString = input()

    if len(encodedString) % 7 == 0:
        print(binaryDecode(encodedString, 7, printBS))

    if len(encodedString) % 8 == 0:
        print(binaryDecode(encodedString, 8, printBS))


if __name__ == "__main__":
    main()
