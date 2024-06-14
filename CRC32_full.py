import bitstring

def reverseBytes(input: bitstring.BitArray):

    for i in range(len(input), 0, -8):
        input.reverse(i-8, i)

    return input

def calculateCRC(message_bitarray: bitstring.BitArray, polynomial_bitarray: bitstring.BitArray):

    print('Original message: \t' + message_bitarray.hex)
    
    # reversing bytes
    message_bitarray = reverseBytes(message_bitarray)

    polynomial_bitarray.prepend('0b1')

    p_len = len(polynomial_bitarray)


    # Adding polynomial_length - 1 zero padding to the message
    message_bitarray.append(p_len - 1)

    # inverting first polynomial_length - 1 bits
    message_bitarray.invert(range(0,p_len - 1))

    m_len = len(message_bitarray)

    padded_polynomial_bitarray = bitstring.BitArray(length=m_len)
    padded_polynomial_bitarray.overwrite(polynomial_bitarray, 0)

    curr_off = 0
    while message_bitarray[:-(p_len - 1)]:
            if not message_bitarray[curr_off]:
                padded_polynomial_bitarray >>=1
                curr_off += 1
                continue
            message_bitarray ^= padded_polynomial_bitarray

    # inverting last polynomial_length - 1 bits
    message_bitarray.invert(range(m_len-(p_len - 1), m_len))

    # reversing bytes
    message_bitarray = reverseBytes(message_bitarray)

    print('Calculated CRC: \t' + message_bitarray[-(p_len-1):].hex)

print('Waiting for hex input: ')
message_string = input()
if not message_string:
    message_bitarray = bitstring.BitArray('0x7085c289317f0c80638e7b7e0800450000548d03000040016beec0a80001c0a8006600000c9900050005e2745d6600000000ecae080000000000101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f3031323334353637')
else:
    message_bitarray = bitstring.BitArray('0x' + message_string)
polynomial_bitarray = bitstring.BitArray('0x04C11DB7')

calculateCRC(message_bitarray, polynomial_bitarray)
