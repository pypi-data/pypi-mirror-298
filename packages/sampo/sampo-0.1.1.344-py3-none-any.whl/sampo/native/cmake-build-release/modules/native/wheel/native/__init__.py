# This file is automaticaly generated for RN-SEISM Python package native.

import os
import sys
import glob
import sysconfig
import importlib
import cpufeature

from ctypes import *


is_windows = os.name == "nt"
is_apple = sys.platform == "darwin"

SHLIB_SUFFIXES = [sysconfig.get_config_var("SHLIB_SUFFIX")]
if not SHLIB_SUFFIXES or not SHLIB_SUFFIXES[0]:
    if is_windows:
        SHLIB_SUFFIXES = [".dll"]
    else:
        SHLIB_SUFFIXES = [".so"]
if is_apple:
    SHLIB_SUFFIXES = [".dylib"]

SHLIB_SUFFIXES.extend(importlib.machinery.all_suffixes())

package_root = os.path.dirname(__file__)
files = []
for suffix in SHLIB_SUFFIXES:
    files.extend(glob.glob('*' + suffix, root_dir=package_root))

if os.name != 'nt':
    flag = True
    counter = 0
    while flag and counter < len(files):
        flag = False
        for f in files:
            try:
                CDLL(os.path.join(package_root, f))
            except:
                continue
            flag = True
            counter += 1


def has_library(name_no_ext: str):
    return bool(list(filter(lambda x: name_no_ext in x, files)))


if cpufeature.CPUFeature['AVX512f'] and cpufeature.CPUFeature['OS_AVX512'] \
        and has_library('native_avx512'):
    from .native_avx512 import *
elif cpufeature.CPUFeature['AVX2'] and cpufeature.CPUFeature['OS_AVX'] \
        and has_library('native_avx2'):
    from .native_avx2 import *
elif cpufeature.CPUFeature['SSE4.2'] and has_library('native_sse4'):
    from .native_sse4 import *
else:
    from .native import *
