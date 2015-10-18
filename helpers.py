"""
CS6238 - Secure Computer Systems
Project Team: Kyle Koza and Anant Lummis

Object Name: helpers.py
Object Functions: long_to_bytes, read_2_lines, modular_lagrange_interpolation, mod_inverse, egcd
Object Description:  The purpose of this object is to incapsulate several helper functions which did not belong in any of the
                     main object classes.
"""

from binascii import unhexlify

def long_to_bytes (val, endianness='big'):
    """
    Use :ref:`string formatting` and :func:`~binascii.unhexlify` to
    convert ``val``, a :func:`long`, to a byte :func:`str`.

    :param long val: The value to pack

    :param str endianness: The endianness of the result. ``'big'`` for
      big-endian, ``'little'`` for little-endian.

    If you want byte- and word-ordering to differ, you're on your own.

    Using :ref:`string formatting` lets us use Python's C innards.
    """

    # one (1) hex digit per four (4) bits
    width = val.bit_length()

    # unhexlify wants an even multiple of eight (8) bits, but we don't
    # want more digits than we need (hence the ternary-ish 'or')
    width += 8 - ((width % 8) or 8)

    # format width specifier: four (4) bits per hex digit
    fmt = '%%0%dx' % (width // 4)

    # prepend zero (0) to the width, to zero-pad the output
    s = unhexlify(fmt % val)

    if endianness == 'little':
        # see http://stackoverflow.com/a/931095/309233
        s = s[::-1]

    return s

#Function read_2_lines(f) reads in two lines at a time from the provided authentication file
def read_2_lines(f):
    for line in f:
        try:
            line2 = f.next()
        except StopIteration:
            line2 = ''

        yield line[:-1], line2[:-1]

#Function modular_lagrange_interpolation(x, points, prime) takes in an x value from a polynomial, several polynomial points, and a 
#large prime number which are all used to perform the Lagrange interpolation function.  This should return a polynomial which can 
#be evaluated to find the Hpwd.
def modular_lagrange_interpolation(x, points, prime):
    # break the points up into lists of x and y values
    x_values, y_values = zip(*points)
    # initialize f(x) and begin the calculation: f(x) = SUM( y_i * l_i(x) )
    f_x = long(0)
    for i in range(len(points)):
        # evaluate the lagrange basis polynomial l_i(x)
        numerator, denominator = 1, 1
        for j in range(len(points)):
            # don't compute a polynomial fraction if i equals j
            if i == j:
                continue
            # compute a fraction & update the existing numerator + denominator
            numerator = (numerator * x_values[j]) % prime
            denominator = denominator * pow((x_values[j] - x_values[i]), prime-2, prime)
        # get the polynomial from the numerator + denominator mod inverse
        lagrange_polynomial = numerator * denominator
        # multiply the current y & the evaluated polynomial & add it to f(x)
        f_x += (y_values[i] * lagrange_polynomial) % prime
    return f_x % prime

#Function mod_inverse(k, prime) takes in a large prime number and the value K and returns the mod inverse.
def mod_inverse(k, prime):
    k = k % prime
    if k < 0:
        r = egcd(prime, -k)[2]
    else:
        r = egcd(prime, k)[2]
    return (prime + r) % prime

#Function egcd(a, b) computes the greatest common denominator between to integers a and b
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
