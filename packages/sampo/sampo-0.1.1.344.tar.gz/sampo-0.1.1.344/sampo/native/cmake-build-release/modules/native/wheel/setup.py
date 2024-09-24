import os
import sys
import shutil
import sysconfig

from glob import glob
from setuptools import setup, findall

from glibc_utils import glibc_version_string


files = [os.path.basename(r) for r in findall('native')]

platform = sysconfig.get_platform()
glibc_version = glibc_version_string()

if glibc_version:
    pos = platform.find('linux')
    if pos >= 0:
        pos += len('linux')
        platform = 'manylinux' + '_' + glibc_version + platform[pos:]

setup(
    name='native',
    version='0.0.2',

    packages=['native'],
    package_data={'native': files},

    # хранить в site-packages в виде архива нельзя, т.к. _c_wrap обращается к __file__
    zip_safe=False,
    script_args=[
        'bdist_wheel',
        '--dist-dir=' + 'C:/Users/Quarter/PycharmProjects/sampo/sampo/native/dist/wheels',
        '--plat-name=' + platform,
        '--python-tag=' + 'cp' + str(sys.version_info.major) + str(sys.version_info.minor)
    ],
    install_requires=["cpufeature>=0.2.1", "numpy"]
)

shutil.rmtree('build', ignore_errors=True)

for match in glob('*.egg-info'):
   shutil.rmtree(match)
