def twos_compliment(decimal: int, bits: int) -> int:
    """
    Decodes a twos compliment int into its signed counterpart

    :param decimal: The unsigned int to be decoded
    :type decimal: int
    :param bits: the range of bits used in the compliment
    :type bits: int
    :return: signed integer
    :rtype: int
    """
    binary_string = f"{decimal:0{bits}b}"
    
    if binary_string[0] != '0':
        decimal = decimal - (1 << bits)
    
    return decimal
