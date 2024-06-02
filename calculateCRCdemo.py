from termcolor import cprint
import time
import bitstring
import argparse

interactive = False
delay = 0.5

def printCRCState(m: str, curr_off: int, p_len: int, p_len_strip: int):
    cprint(m[: curr_off], 'green', end='')
    # cprint(len(m[: curr_off]), 'green', end='\n')

    if curr_off+p_len_strip > len(m) - (p_len_strip - 1):
        cprint(m[curr_off : len(m)-(p_len - 1)], 'red', end='')
        # cprint(len(m[curr_off : len(m)-(p_len - 1)]), 'red', end='\n')
    else:
        cprint(m[curr_off : curr_off + p_len_strip], 'red', end='')
        # cprint(len(m[curr_off : curr_off + p_len]), 'red', end='\n')
    
    cprint(m[curr_off + p_len_strip:-(p_len - 1)], 'green', end='')
    # cprint(len(m[curr_off + p_len:-(p_len - 1)]), 'green', end='\n')
    cprint(m[-(p_len - 1) :], 'blue', end='\n')
    # cprint(len(m[-(p_len - 1) :]), 'blue', end='\n\n')

def printPoly(p: str, curr_off: int):
    cprint(curr_off * ' ', end='')
    cprint(p, 'red', end='\n')


def getCRC(message_bitstring: str, polynomial_bitstring: str):
    
    polynomial_bitstring = '1' + polynomial_bitstring

    m_len = len(message_bitstring)
    p_len = len(polynomial_bitstring)

    
    # Adding poly_len - 1 zero padding to the message
    m = message_bitstring + '0' * (p_len - 1)
    
    # Removing leading zeros from the polynomial
    p = polynomial_bitstring.lstrip('0')
    p_len_strip = len(p)

    curr_off = 0

    while int(m[:m_len], 2):

        if m[curr_off] == '0':
            if interactive: print('Skipping...')
            curr_off += 1
            continue

        if interactive:
            printCRCState(m, curr_off, p_len, p_len_strip)
            printPoly(p, curr_off)
            time.sleep(delay)

        m = m[: curr_off] + format(int(m[curr_off : curr_off+p_len_strip], 2) ^ int(p, 2), '0' + str(p_len_strip) + 'b') + m[curr_off+p_len_strip :]


        curr_off += 1

    print(hex(int(m[-(p_len - 1):], 2)))



parser = argparse.ArgumentParser(description='Calculates CRC value of a given text input.')
parser.add_argument('input_txt', metavar='TEXT', type=str, nargs=1, help='Text to be given to the CRC calculator.')
parser.add_argument('input_poly', metavar='POLYNOMIAL', type=str, nargs=1, help='Polynomial in hexadecimal form.')
parser.add_argument('-i', '--interactive', action="store_true", help='Interactive display of CRC calculation.', required=False)
parser.add_argument('-d', '--delay', metavar='DELAY', type=float, nargs=1, help='Delay in seconds between lines in interactive mode.', required=False)

args = parser.parse_args()

interactive = args.interactive

if args.delay: delay = args.delay[0]


try:
    int(args.input_poly[0], 16)
except ValueError:
    print("Incorrect polynomial form.")
    exit()

poly_string = format(hex(int(args.input_poly[0], 16)))

msg = bitstring.BitArray(args.input_txt[0].encode('utf-8'))
poly = bitstring.BitArray(poly_string)
getCRC(msg.bin, poly.bin)
