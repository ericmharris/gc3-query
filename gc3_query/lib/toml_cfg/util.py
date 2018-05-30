

def quote_key(s: str) -> str:
    """Takes a sinlge string of TOML and returns it with the key value quoted to allow more flexibility in names.

    key_name = value  -> 'key_name' = value
    key name = value  -> 'key name' = value

    :param s:
    """


