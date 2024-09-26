import abc
import difflib
import io
import os
import pickle
from collections.abc import Callable
from pprint import pprint
from typing import Any, Type, Union

import pytest


class BaseSnapshotHandler(abc.ABC):
    def __init__(
        self,
        handler_options: dict[str, Any],
        pytest_config: Type[pytest.Config],
        tw: int,
    ) -> None: ...

    @abc.abstractmethod
    def save(self, folder: Union[str, os.PathLike], obj: Any) -> None: ...

    @abc.abstractmethod
    def load(self, folder: Union[str, os.PathLike]) -> Any: ...

    @abc.abstractmethod
    def show(self, obj: Any) -> list[str]: ...

    @abc.abstractmethod
    def compare(self, current_obj: Any, recorded_obj: Any) -> bool: ...

    @abc.abstractmethod
    def show_differences(
        self, current_obj: Any, recorded_obj: Any, has_markup: bool
    ) -> list[str]: ...


snapshot_handlers: list[tuple[Callable[[Any], bool]]] = []


class PythonObjectHandler(BaseSnapshotHandler):
    def __init__(self, handler_options, pytest_config, tw):
        self.compact = handler_options.get("compact", False)

    def save(self, folder, obj):
        with open(os.path.join(folder, "object.pkl"), "wb") as fh:
            pickle.dump(obj, fh)

    def load(self, folder):
        with open(os.path.join(folder, "object.pkl"), "rb") as fh:
            return pickle.load(fh)

    def show(self, obj):
        stream = io.StringIO()
        pprint(obj, stream=stream, compact=self.compact)
        return stream.getvalue().splitlines()

    def compare(self, current_obj, recorded_obj):
        return recorded_obj == current_obj

    def show_differences(self, current_obj, recorded_obj, has_markup):
        return list(
            difflib.unified_diff(
                self.show(current_obj),
                self.show(recorded_obj),
                "current",
                "expected",
                lineterm="",
            )
        )


snapshot_handlers.append(
    (
        lambda obj: isinstance(obj, (int, float, str, list, tuple, dict, set)),
        PythonObjectHandler,
    ),
)
