

def quote_key(s: str) -> str:
    """Takes a sinlge string of TOML and returns it with the key value quoted to allow more flexibility in names.

    key_name = value  -> 'key_name' = value
    key name = value  -> 'key name' = value

    :param s:
    """
    first_eq_loc = s.find('=')
    if first_eq_loc == -1:
        return s
    lhs = s[0:first_eq_loc-1].strip()
    rhs = s[first_eq_loc+1:].strip()
    return f"'{lhs}' = {rhs}"



