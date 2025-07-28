import string

ALPHABET = string.digits + string.ascii_uppercase
MAX_BASE = len(ALPHABET)
MASK = '1A2B3C'


def encode(number):
    """
    Encode number to alphabet
    """
    try:
        return ALPHABET[number]
    except IndexError:
        raise Exception("Can't encode: {}".format(number))


def decode(value):
    """
    Decode alphabet to number
    """
    try:
        return ALPHABET.index(value)
    except ValueError:
        raise Exception("Can't decode: {}".format(value))


def dec_to_base(dec=0, base=MAX_BASE):
    """
    Recursive function to convert number to base numeric system

    Example:
        number = 99,
        base = 16

        Repeat:
            99 divided by base is 99/16 = 6 remainder 3. So d=6 and r=3. So m=3 and the new number is 6.
            6 divided by base is  6/16 = 0 remainder 6. So d=0 and r=6. So m=63 and the new n is 0.

            So 99 (base=10) is 63 (base=16)
    """
    if dec < base:
        return encode(dec)
    else:
        return dec_to_base(dec // base, base) + encode(dec % base)


def base_to_dec(value, base=MAX_BASE, pow_value=0):
    """
    Recursive function to convert number in base numeric system to decimal numeric system

    Example:
        s = '104'
        formula = (1 × 10^2) + (0 × 10^1) + (4 × 10^0)
    """
    if value == "":
        return 0
    else:
        return decode(value[-1]) * (base ** pow_value) + base_to_dec(value[0:-1], base, pow_value + 1)


def normalize(value, length=6):
    """
    Normalize string to specified length
    Return normalized string and count of random letters, assigned as suffix
    """
    string_len = len(str(value))

    # already normalized
    if string_len == length:
        return value
    elif string_len < length:
        diff = length - string_len
        prefix = ''.join('0' for i in range(diff))
        return f"{prefix}{value}"
    else:
        raise Exception("Can't normalize to length: {}".format(length))


def denormalize(value, suffix_count, **kwargs):
    """
    Remove random generated suffix from the normalized number
    """
    if suffix_count == 0:
        return base_to_dec(value, **kwargs)
    value = value[:-suffix_count]
    return base_to_dec(value, **kwargs)


def mask_to_dec(**kwargs):
    return base_to_dec(MASK, **kwargs)
