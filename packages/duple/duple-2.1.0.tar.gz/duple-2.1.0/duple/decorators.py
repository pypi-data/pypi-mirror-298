import cProfile
import functools
import pstats
from time import perf_counter

from duple.app_logging import logger, setup_logging

setup_logging()


def profile(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        try:
            retval = func(*args, **kwargs)
        finally:
            profiler.disable()
            with open("profile.out", "w") as profile_file:
                stats = pstats.Stats(profiler, stream=profile_file)
                stats.print_stats()
        return retval

    return inner


def log_func_with_args(func):
    start = perf_counter()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.debug(f"function {func.__module__}/{func.__qualname__} called with args {signature}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} completed execution in {(perf_counter() - start): .5f}")
            return result
        except Exception as e:
            logger.exception(f"Exception raised in function {func.__module__}/{func.__qualname__}, exception: {str(e)}")
            raise e

    return wrapper


def log_func_time(func):
    start = perf_counter()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            logger.debug(
                f"function {func.__module__}/{func.__qualname__} completed execution in {(perf_counter() - start): .5f}"
            )
            return result
        except Exception as e:
            logger.exception(f"Exception raised in function {func.__module__}/{func.__qualname__}, exception: {str(e)}")
            raise e

    return wrapper
