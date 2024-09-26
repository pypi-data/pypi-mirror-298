from random import choice
from string import ascii_letters, digits
from typing_extensions import LiteralString


class Storage[T](dict[str, T]):
    """
    A generic storage class that extends a dictionary to hold items of any type,
    identified by unique string keys. It provides functionality to automatically
    generate unique keys for items if not provided.

    Type Parameters:
        T: The type of the items to be stored in the dictionary.

    Methods:
        __init__(): Initializes a new instance of the storage.
        _get_unique_key(): Generates a unique key for storing an item.
        append(item: T, key: str = None): Adds an item to the storage with an optional key.
    """
    def __init__(self, choices: LiteralString = ascii_letters + digits, length: int = 16) -> None:
        """
        Initializes the storage with an empty dictionary.
        """
        super().__init__()
        self.choices = choices
        self.length = length

    def _get_unique_key(self) -> str:
        """
        Generates a unique key composed of random letters and digits.

        Returns:
            A unique string key of 16 characters.
        """
        while True:
            key = ''.join(choice(self.choices) for _ in range(self.length))
            if key not in self:
                return key

    def append(self, item: T, key: str | None = None) -> str:
        """
        Adds an item to the storage with an automatically generated or specified key.
        If the key already exists in the storage, a KeyError is raised.

        Parameters:
            item: The item to be stored.
            key (Optional[str]): The key under which to store the item. If None, a unique key
                                 is generated automatically.

        Returns:
            The key used to store the item in the dictionary.

        Raises:
            KeyError: If the specified key already exists in the storage.
        """
        if key is None:
            key = self._get_unique_key()
        elif key in self:
            raise KeyError("Key already exists")
        self[key] = item
        return key
