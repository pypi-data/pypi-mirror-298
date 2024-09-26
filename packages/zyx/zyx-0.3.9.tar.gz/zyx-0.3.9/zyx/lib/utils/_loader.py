import builtins
from rich import print
from types import ModuleType
from typing import Any, Optional, TypeVar
from functools import wraps, lru_cache
import threading
import asyncio
from concurrent.futures import ProcessPoolExecutor
from importlib import import_module, util
import inspect

# Replace the default print with rich's print for better visibility
builtins.print = print

T = TypeVar("T")
R = TypeVar("R")


class LazyLoaderMeta(type):
    """
    Meta class for lazy loading attributes from a module.
    Optimized with advanced caching and lock-free techniques.
    """

    @lru_cache(maxsize=None)  # Cache the getattr results for faster lookup
    def __getattr__(cls, name: str) -> Any:
        module = cls._load()
        return getattr(module, name)

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        module = cls._load()
        return module(*args, **kwargs)


class loader(metaclass=LazyLoaderMeta):
    """
    Lazy loader for a module.
    Utilizes lock-free optimizations and multiprocessing for performance.
    """

    _module_cache: Optional[ModuleType] = None
    _executor = ProcessPoolExecutor(max_workers=1)
    _async_lock = asyncio.Lock()  # Asyncio lock for async preloading

    @classmethod
    async def preload(cls):
        async with cls._async_lock:
            await asyncio.to_thread(cls._load)

    # Fast loading using importlib.util and avoiding redundant imports
    @classmethod
    def _load(cls) -> Any:
        if cls._module_cache is None:
            # Double-checked locking pattern
            if cls._module_cache is None:
                try:
                    # Check if module is already loaded
                    module_spec = util.find_spec(cls._module_name)
                    if module_spec is not None:
                        module = import_module(cls._module_name)
                        cls._module_cache = getattr(module, cls._attr_name)

                        # Handle wrapping for generators and functions
                        if inspect.isclass(cls._module_cache):
                            return type(cls.__name__, (cls._module_cache,), {})
                        elif inspect.isgeneratorfunction(cls._module_cache):
                            return cls._module_cache  # No wrapping necessary
                        elif inspect.isfunction(cls._module_cache):
                            return cls._module_cache  # No wrapping necessary
                except (ImportError, AttributeError) as e:
                    raise e
        return cls._module_cache

    @classmethod
    def init(cls, module_name: str, attr_name: str) -> None:
        cls._module_name = module_name
        cls._attr_name = attr_name

    def __getattr__(self, name: str) -> Any:
        module = self._load()
        return getattr(module, name)

    def __iter__(self):
        module = self._load()
        if hasattr(module, "__iter__"):
            return iter(module)
        raise TypeError(f"{module} object is not iterable")

    def __next__(self):
        module = self._load()
        if hasattr(module, "__next__"):
            return next(module)
        raise TypeError(f"{module} object is not an iterator")

    def __getitem__(self, item):
        module = self._load()
        if hasattr(module, "__getitem__"):
            return module[item]
        raise TypeError(f"{module} object does not support indexing")

    def __len__(self):
        module = self._load()
        if hasattr(module, "__len__"):
            return len(module)
        raise TypeError(f"{module} object does not have a length")

    def __contains__(self, item):
        module = self._load()
        if hasattr(module, "__contains__"):
            return item in module
        raise TypeError(f"{module} object does not support membership test")

    # Start preloading the module asynchronously using multiprocessing
    @classmethod
    def start_preloading(cls):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(cls.preload())
