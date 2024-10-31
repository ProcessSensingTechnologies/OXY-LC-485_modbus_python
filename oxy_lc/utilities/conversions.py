def twos_compliment(decimal: int, bits: int) -> int:
    binary_string = f"{decimal:0{bits}b}"
    
    if binary_string[0] != '0':
        decimal = decimal - (1 << bits)
    
    return decimal
