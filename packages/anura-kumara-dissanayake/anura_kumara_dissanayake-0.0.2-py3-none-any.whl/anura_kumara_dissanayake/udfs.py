class ExpectedStringArgument(ValueError):
    pass


def get_percentage_of_nonalphabetical_characters(search_term: str) -> float:
    """
    Takes a string containing an arbitrary combination of numeric, alphabetic
    and other characters, and returns the percentage thereof over the total
    length of the input string.

    Parameters
    ----------
    search_term: str
        An input string containing an arbitrary combination of numeric,
        alphabetic and other characters.

    Return
    ------
    float: The percentage of non-alphabetical characters in the input string.

    Examples
    --------
    >>> f = get_percentage_of_nonalphabetical_characters
    >>> assert f("letters") == 0.0
    >>> assert f("0414") == 1.0
    >>> try:
    ...   f(3)
    ... except ValueError:
    ...   assert True
    >>> assert f("a different kind of string") == 0.1538
    """
    if not isinstance(search_term, str):
        raise ExpectedStringArgument(
            f"Expected a string as input, got {type(search_term)}."
        )
    if not search_term:
        return 0.0
    n_chars = len(search_term)
    n_unk = len([ch for ch in list(search_term) if not ch.isalpha()])
    return round(n_unk / n_chars, 4)


if __name__ == "__main__":
    from doctest import testmod
    testmod()

