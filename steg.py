#!/usr/bin/env python3

import sys, getopt

def decodeBytes(coverData: bytes, interval: int, start: int):

    hiddenData = b''
    sentinal = b'\x00\xff\x00\x00\xff\x00'
    senMatch = 0

    for i in range(start, len(coverData)+1, interval):

        #Sentinal handling
        #Keep track of the last sentinal character seen
        if coverData[i] == sentinal[senMatch]:
            senMatch += 1
            if senMatch > 5:
                break
        #if we don't see the next sentinal character,
        #reset to the beginning of the sentinal and
        #dump the last couple of sentinal characters we've seen
        elif senMatch > 0:
            hiddenData += sentinal[:senMatch]
            senMatch = 0
            hiddenData += bytes([coverData[i]])
        else:
            hiddenData += bytes([coverData[i]])

    if senMatch < 6:
        print("WARN: Reached end of file without finding sentinal", file=sys.stderr)
    return hiddenData

def encodeBytes(hiddenData: bytes, coverData: bytes, interval: int, start: int) -> bytearray:

    encoded = bytearray(coverData)
    hiddenData += b'\x00\xff\x00\x00\xff\x00'

    end = start + len(hiddenData) * interval

    #Check that hidden data fits in wrapper
    if len(coverData) < end:
        print('ERROR: Hidden file does not fit in cover file', file=sys.stderr)
        print(f'Hidden file needs {end} bytes of space, cover file is {len(coverData)} bytes', file=sys.stderr)
        sys.exit(2)

    #Do the thing
    for coverDex, hiddenDex in zip(range(start, end, interval), range(len(hiddenData))):
        encoded[coverDex] = hiddenData[hiddenDex]

    return encoded

def decodeBits(coverData: bytes, interval: int, start: int, msb:bool = True):
    sentinal = b'\x00\xff\x00\x00\xff\x00'
    decodedData = b''

    bit = 7 if msb else 0
    workingByte = bytearray(b'\x00')

    for coverByte in coverData[start::interval]:
        workingByte[0] |= (coverByte & 0x01) << bit

        #When the working byte is full, shove it onto our data and reset it
        if msb and bit == 0 or not msb and bit == 7:
            decodedData += bytes(workingByte)
            workingByte[0] = 0x00

            if len(decodedData) > 5 and decodedData[-6:] == sentinal:
                return decodedData[:-6]

        bit = (bit + (-1 if msb else 1)) % 8

    print("WARN: Reached end of cover file without finding sentinal. Data could be corrupted.", file=sys.stderr)
    return decodedData

def encodeBits(hiddenData: bytes, coverData: bytes, interval: int, start: int, msb: bool = True):

    hiddenData += b'\x00\xff\x00\x00\xff\x00'

    end = start + (len(hiddenData) * interval * 8)

    if len(coverData) < end:
        print('ERROR: Hidden file does not fit in cover file', file=sys.stderr)
        print(f'Hidden file needs {end} bytes of space, cover file is {len(coverData)} bytes', file=sys.stderr)
        sys.exit(2)

    encoded = bytearray(coverData)

    bitDex = 7 if msb else 0
    byteDex = 0

    for coverDex in range(start, end, interval):
        bit = (hiddenData[byteDex] >> bitDex) & 0x1
        encoded[coverDex] = (encoded[coverDex] & 0xfe) | bit

        bitDex += -1 if msb else 1
        if bitDex > 7 or bitDex < 0:
            bitDex %= 8
            byteDex += 1

    return bytes(encoded)



def main():

    usageString = f"Usage: {sys.argv[0]} -(sr) -(bB) -o<val> [-i<val>] -w<val> [-h<val>]"
    longUsageString = usageString + """

Required Options:
    s|r : [s]tore or [r]ead hidden data
    b|B : Use [b]it mode or [B]yte mode
    w   : Wrapper file in which data will be hidden
    h   : Hidden file to be stored (only in store mode)

Optional Arguments:
    i   : Interval (How many bytes to skip between hidden data)
    o   : Offset (Byte at which data begins in wrapper file)
    O   : Output (Default: overwrite wrapper file)
    """

    read = True
    byte = False
    offset = 0
    interval = 1
    wrapper = None
    hidden = None
    output = None

    #argument parsing
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "srbBo:i:w:hO:", ['help'])
    except getopt.GetoptError as msg:
        print(msg, file=sys.stderr)
        print(usageString, file=sys.stderr)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "--help":
            print(longUsageString)
            sys.exit()
        elif opt == "-s":
            read = False
        elif opt == "-r":
            read = True
        elif opt == "-b":
            byte = False
        elif opt == "-B":
            byte = True
        elif opt == "-o":
            offset = int(arg)
        elif opt == "-i":
            interval = int(arg)
        elif opt == "-w":
            wrapper = arg
        elif opt == "-h":
            hidden = arg
        elif opt == "-O":
            output = arg

    if wrapper is None:
        print("ERROR: No wrapper file specified", file=sys.stderr)
        print(usageString, file=sys.stderr)
        exit(1)

    if output is None:
        output = wrapper

    if read:
        with open(wrapper, 'rb') as wrapperFile:
            if byte:
                sys.stdout.buffer.write(decodeBytes(wrapperFile.read(), interval, offset))
            else:
                sys.stdout.buffer.write(decodeBits(wrapperFile.read(), interval, offset))
    elif hidden is None:
        print("ERROR: No hidden file specified", file=sys.stderr)
        print(usageString, file=sys.stderr)
        exit(1)
    else:
        with open(hidden, 'rb') as hiddenFile:
            with open(wrapper, 'rb') as wrapperFile:
                if byte:
                    newWrapper = encodeBytes(hiddenFile.read(), wrapperFile.read(), interval, offset)
                else:
                    newWrapper = encodeBits(hiddenFile.read(), wrapperFile.read(), interval, offset)
            with open(output, 'wb') as newFile:
                newFile.write(newWrapper)

if __name__ == '__main__':
    main()
