from typing import Callable, Any
from collections import defaultdict


class NormalizedDefaultDict[KT: str, VT](defaultdict[KT, VT]):
    def __init__(
            self,
            default_factory: Callable[[], VT] | None = None,
            /,
            *args,
            normalization: Callable[[Any], KT] | None = None,
            **kwargs
    ) -> None:
        self._normalization = normalization or self._default_normalization

        if args and isinstance(args[0], dict):
            normalized_dict = {self._normalization(k): v for k, v in args[0].items()}
            args = (normalized_dict, *args[1:])
        super().__init__(default_factory, *args, **kwargs)

    def __setitem__(self, key: KT, value: VT) -> None:
        key = self._normalization(key)
        super().__setitem__(key, value)

    def __getitem__(self, key: KT) -> VT:
        key = self._normalization(key)
        return super().__getitem__(key)

    @staticmethod
    def _default_normalization(key: KT) -> str:
        return key.lower()

    def update(self, *args, **kwargs) -> None:
        for k, v in dict(*args, **kwargs).items():
            self[k] = v
