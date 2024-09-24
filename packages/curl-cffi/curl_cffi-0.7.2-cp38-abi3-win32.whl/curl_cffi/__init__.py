"""""" # start delvewheel patch
def _delvewheel_patch_1_8_2():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'curl_cffi.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-curl_cffi-0.7.2')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-curl_cffi-0.7.2')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_8_2()
del _delvewheel_patch_1_8_2
# end delvewheel patch

__all__ = [
    "Curl",
    "AsyncCurl",
    "CurlMime",
    "CurlError",
    "CurlInfo",
    "CurlOpt",
    "CurlMOpt",
    "CurlECode",
    "CurlHttpVersion",
    "CurlSslVersion",
    "CurlWsFlag",
    "ffi",
    "lib",
]

import _cffi_backend  # noqa: F401  # required by _wrapper

from .__version__ import __curl_version__, __description__, __title__, __version__  # noqa: F401

# This line includes _wrapper.so into the wheel
from ._wrapper import ffi, lib
from .aio import AsyncCurl
from .const import (
    CurlECode,
    CurlHttpVersion,
    CurlInfo,
    CurlMOpt,
    CurlOpt,
    CurlSslVersion,
    CurlWsFlag,
)
from .curl import Curl, CurlError, CurlMime
