def text_compression(text:str, symbol:str, symbol_range:int = DEFAULT_COUNT)->str:
    for i in range(symbol_range):
        n = symbol_range - i + 1
        text = text.replace(f"{symbol}"*n, symbol)
    return text

def text_newline_compression(text, symbol_range = DEFAULT_COUNT):
    return text_compression(text, NEWLINE, symbol_range)

def text_whitespace_compression(text, symbol_range = DEFAULT_COUNT, abnormal=True):
    """'Remove whitespace' and 'replace newlines to whitespace' from a string."""
    case = [SPACE]
    if abnormal:
        case.append(SPACE_ZENKAKU)
        case.append(TAB)
    for s in case:
        text = text_compression(text, s, symlbol_range)
    return text