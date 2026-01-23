def text_replace(text:str, from_symbols:list, to_symbols:list or str)->str:
    
    """
    Replace specific symbols in a text string.

    Args:
        text (str): Target text to replace symbols.
        from_symbols (list): List of symbols to replace.
        to_symbols (list or str): List of symbols to replace with, or a single str to replace all symbols with.

    Returns:
        str: Text string with replaced symbols.
    """
    if isinstance(from_symbols, str):
        from_symbols = [from_symbols]
    if isinstance(to_symbols, str):
        to_symbols = [to_symbols*len(from_symbols)]

    for from_text, to_text in zip(from_symbols, to_symbols):
        text = text.replace(from_text, to_text)
    return text