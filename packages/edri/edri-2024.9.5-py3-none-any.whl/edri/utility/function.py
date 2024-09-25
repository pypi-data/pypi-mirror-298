from typing import Iterable, TypeVar, Callable, Any

T = TypeVar("T")

def camel2snake(title: str) -> str:
    """
    Converts a camelCase string to a snake_case string.

    Parameters:
        title (str): The camelCase string to be converted.

    Returns:
        str: The converted snake_case string.

    Examples:
        >>> camel2snake("camelCaseExample")
        'camel_case_example'
        >>> camel2snake("CamelCaseExample")
        'camel_case_example'
    """
    new_title = ""
    underscore = False
    for letter in title:
        if 65 <= ord(letter) <= 90:
            if underscore:
                new_title += '_'
                underscore = False
            new_title += chr(ord(letter) + 32)
        else:
            underscore = True
            new_title += letter
    return new_title


def snake2camel(title: str, /, *, exceptions: tuple[str, ...] | None = None) -> str:
    """
    Converts a snake_case string to a camelCase string, with optional exceptions
    where the conversion should not be applied.

    Parameters:
        title (str): The snake_case string to be converted.
        exceptions (Optional[tuple[str]]): A tuple of strings that, when matched at the
                                      beginning of the title, prevent conversion and
                                      return the title as is. Defaults to None.

    Returns:
        str: The converted camelCase string if no exception is matched; otherwise,
             the original string.

    Examples:
        >>> snake2camel("snake_case_example")
        'snakeCaseExample'
        >>> snake2camel("id_example", exceptions=("id_",))
        'id_example'

    Notes:
        - The first segment of the snake_case string remains lowercase, aligning
          with the camelCase convention.
        - If the title starts with any of the specified exceptions, it is returned
          unchanged, useful for preserving certain identifiers.
    """
    if exceptions is None:
        exceptions = ("id_",)
    if title.startswith(exceptions):
        return title
    title_list = title.split('_')
    title_list = [title_list[0]] + [word[0].upper() + word[1:] for word in title_list][1:]
    return ''.join(title_list)


def partition(pred: Callable[[T], bool], iterable: Iterable) -> tuple[list[T], list[T]]:
    """
    Splits an iterable into two lists based on a predicate function.

    Args:
        pred (Callable[[T], bool]): A function that takes an item and returns a boolean value.
                                    Items for which this function returns True will go into the
                                    first list; items for which it returns False will go into the
                                    second list.
        iterable (Iterable): The iterable to be partitioned.

    Returns:
        tuple[list[T], list[T]]: A tuple containing two lists:
            - The first list contains all items from the iterable for which `pred` returned True.
            - The second list contains all items from the iterable for which `pred` returned False.

    Example:
        >>> partition(lambda x: x % 2 == 0, [1, 2, 3, 4])
        ([2, 4], [1, 3])
    """
    trues = []
    falses = []
    for item in iterable:
        if pred(item):
            trues.append(item)
        else:
            falses.append(item)
    return trues, falses

def format_url(url: str, **kwargs: dict[str, Any]) -> str:
    """
    Formats a URL string by replacing placeholders with keyword arguments. If a parameter is missing,
    it is considered optional only if it appears at the end of the URL or if all subsequent placeholders
    are also missing. Otherwise, raises a KeyError.

    Args:
        url (str): The URL template containing placeholders in the format `{placeholder}`.
        **kwargs: Keyword arguments representing the replacement values for the placeholders in the URL.

    Returns:
        str: The formatted URL with all placeholders replaced by their corresponding values.
             If optional parameters are missing, trailing placeholders are removed.

    Raises:
        KeyError: If a required URL parameter is missing, and it is not at the end of the URL,
                  or if other placeholders to the right are provided.

    Examples:
        >>> format_url('https://example.com/{user}/{id}', user='john', id=42)
        'https://example.com/john/42'

        Missing an optional trailing parameter:
        >>> format_url('https://example.com/{user}/{id}', user='john')
        'https://example.com/john'

        Missing a parameter that makes the rest optional:
        >>> format_url('https://example.com/{user}/{id}/{page}', user='john')
        'https://example.com/john'

        Raises KeyError if a non-trailing parameter is missing:
        >>> format_url('https://example.com/{user}/{id}/detail', user='john')
        KeyError: 'Optional url parameter is missing: id'

        Raises KeyError when a middle parameter is missing, but a subsequent parameter is present:
        >>> format_url('https://example.com/{user}/{id}/{page}', user='john', page='home')
        KeyError: 'Optional url parameter is missing: id'
    """
    class Helper(dict):
        def __init__(self, **kwargs) -> None:
            super().__init__(kwargs)
            self.missing = []

        def __missing__[KT](self, key: KT) -> KT:
            self.missing.append(key)
            return key

    kwargs = Helper(**kwargs)
    formated_url = url.format_map(kwargs)
    for missing in reversed(kwargs.missing):
        if formated_url.endswith(f"/{missing}"):
            formated_url = formated_url.removesuffix(f"/{missing}")
        else:
            raise KeyError("Optional url parameter is missing: %s" % missing)
    return formated_url
