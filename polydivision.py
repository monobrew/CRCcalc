def xor_hex(hex_reminder):
    # Remove the '0x' prefix and convert to an integer
    reminder_value = int(hex_reminder, 16)
    
    # Perform the XOR operation
    xor_value = reminder_value ^ 0xFFFFFFFF
    
    # Calculate the required length of the output (number of hex digits in original hex_reminder)
    length = len(hex_reminder) - 2  # Subtracting 2 to remove the '0x' part
    
    # Format the result ensuring leading zeros are included
    xor_reminder = f"0x{xor_value:0{length}X}"
    
    return xor_reminder

def _hex_to_binary(hex_string):
    # Convert hexadecimal string to integer
    hex_number = int(hex_string, 16)
    
    # Convert integer to binary string and remove the '0b' prefix
    binary_string = bin(hex_number)[2:]
    
    # Pad the binary string with leading zeros to ensure it has 8 bits per hexadecimal digit
    padded_binary_string = binary_string.zfill(len(hex_string) * 4)
    
    return padded_binary_string

def _binary_to_hex(binary_string):
    # Convert binary string to integer
    decimal_number = int(binary_string, 2)
    
    # Convert integer to hexadecimal string
    hex_string = hex(decimal_number)[2:]
    
    # Ensure the hexadecimal string has even length by padding with leading zero if necessary
    if len(hex_string) % 2 != 0:
        hex_string = '0' + hex_string
    
    return hex_string

def _binary_to_hex2(binary_str):
    # Convert binary string to integer
    integer_value = int(binary_str, 2)
    
    # Calculate the length of the hexadecimal representation
    hex_length = (len(binary_str) + 3) // 4  # Each hex digit represents 4 binary digits
    
    # Convert integer to hexadecimal string and format it
    hex_str = f"0x{integer_value:0{hex_length}X}"
    
    return hex_str

def _polynomial_division(msg, polynomial):
    # Convert integers to binary strings
    msg_bin = bin(msg)[2:]
    polynomial_bin = bin(polynomial)[2:]
    
    # Initialize quotient and remainder
    quotient = 0
    remainder = msg
    
    # Get the degree of the polynomial
    degree_polynomial = len(polynomial_bin) - 1
    
    # Perform polynomial division
    while len(bin(remainder)[2:]) >= len(polynomial_bin):
        # Determine the degree of the current remainder
        degree_remainder = len(bin(remainder)[2:]) - 1
        
        # Determine the factor to multiply polynomial by (shift polynomial)
        shift = degree_remainder - degree_polynomial
        factor = 1 << shift
        
        # Update quotient
        quotient ^= factor
        
        # Subtract the shifted polynomial from the remainder
        remainder ^= polynomial << shift
    
    return quotient, remainder

def _reverse_hex(hex_number):

    if hex_number.startswith("0x"):
        hex_number = hex_number[2:]
        
    bin = _hex_to_binary(hex_number)

    rev_bin = bin[::-1]

    reversed_hex_number = _binary_to_hex2(rev_bin)

    return reversed_hex_number

def CRC(msg, polymonal):
    
    rev_msg = _reverse_hex(msg)

    pad_rev_msg = rev_msg + '00000000'

    first_4_bytes = pad_rev_msg[:10]

    other_bytes = pad_rev_msg[10:]

    xor_msg = hex(int(first_4_bytes, 16) ^ 0xFFFFFFFF) + other_bytes

    quotient, reminder = _polynomial_division(int(xor_msg, 16), polymonal)

    hex_reminder = hex(reminder)

    xor_reminder = xor_hex(hex_reminder)

    crc_checksum = _reverse_hex(xor_reminder)

    return crc_checksum

checksum = CRC('ff2', 0x104C11DB7)

print(f"{checksum = }")

