#!/usr/bin/env python3
import sys, getopt

keyFile = 'key'

# Argument parsing
try:
    opts, args = getopt.gnu_getopt(sys.argv[1:], "k:", [])
except getopt.GetoptError as e:
    print(e, file=sys.stderr)
    sys.exit(1)

for opt, arg in opts:
    if opt == '-k':
        keyFile = arg


try:
    with open(keyFile , 'rb') as f:
        key = f.read()
except FileNotFoundError:
    print("Key file not found", file=sys.stderr)
    exit(2)

#Message must be read as bytes, so can't use input()
message = sys.stdin.buffer.read()

#Error checking
if len(key) != len(message):
    print(f'got {len(key)}-byte key and {len(message)}-byte message', file=sys.stderr)
    print("Key and message do not have matching length, cannot perform XOR", file=sys.stderr)
    sys.exit(2)

#Do the thing
cipher = bytes([a ^ b for a,b in zip(key, message)])

sys.stdout.buffer.write(cipher)
