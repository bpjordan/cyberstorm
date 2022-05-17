#!/usr/bin/env python3

import sys, getopt, pytz
from hashlib import md5
from datetime import datetime, timezone

DEBUG = 0

def main():
    epochText = None
    central = pytz.timezone('US/Central')
    now = datetime.now()

    #Argument parsing
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "e:d:v", ["epoch=", "debugTime="])
    except getopt.GetoptError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    for opt, arg in opts:
        if opt in ["-e", "--epoch"]:
            epochText = arg
        elif opt in ["-d", "--debugTime"]:
            try:
                now = datetime.strptime(arg, "%Y %m %d %H %M %S")
            except ValueError:
                print(f"Couldn't parse '{arg}' into a date.", file=sys.stderr)
                print(f"Date Format: 'YYYY MM DD HH mm SS'", file=sys.stderr)
                sys.exit(2)
        elif opt == "-v":
            global DEBUG
            DEBUG += 1


    #If we weren't given the epoch as an argument, get it from stdin
    if epochText is None:
        epochText = input()

    try:
        epoch = datetime.strptime(epochText, "%Y %m %d %H %M %S") #parse epoch
    except ValueError:
        print(f"Couldn't parse '{arg}' into a date.", file=sys.stderr)
        print(f"Date Format: 'YYYY MM DD HH mm SS'", file=sys.stderr)
        sys.exit(2)

    #Both times are naive, so we need to let them know that DST is a thing
    now, epoch = central.localize(now, is_dst=True), central.localize(epoch, is_dst=True)

    #Now we can take the difference between their timestamps from the UNIX epoch
    diff = int(now.timestamp() - epoch.timestamp())
    hashtime = diff // 60 * 60  #get the 60sec interval

    #Actually taking the hash is of course a chore as well
    hsh = md5(md5(str(hashtime).encode()).hexdigest().encode()).hexdigest()

    if DEBUG > 0:
        print(f"System:\t{now}", file=sys.stderr)
        print(f"Epoch:\t{epoch}", file=sys.stderr)
        print(f"Difference: {diff}")
        print(f"Interval: {hashtime}")
        print(f"Hash: {hsh}", file=sys.stderr)

    #Construction of code
    code = ''
    for char in hsh:
        if char.isalpha():
            code += char
            if len(code) == 2:
                break
    for char in hsh[::-1]:
        if char.isdigit():
            code += char
            if len(code) == 4:
                break

    print(code)



if __name__ == '__main__':
    main()
