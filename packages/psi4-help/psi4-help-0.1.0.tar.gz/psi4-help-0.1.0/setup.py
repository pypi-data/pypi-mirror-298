from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

here = os.path.abspath(os.path.dirname(__file__))

package_data = {
    'psi4_help': ['psi4_keywords.yaml'], 
}

def run_psi4_help():
    from psi4_help.psi4_help import Psi4KeywordsCLI
    cli = Psi4KeywordsCLI()
    cli.cmdloop()

entry_points = {
    'console_scripts': [
        'psi4-help=psi4_help.__main__:run_psi4_help',
    ],
}
setup(
    name="psi4-help",
    version="0.1.0",
    author="F.L. Wang",
    author_email="FL058@foxmail.com",
    description="A helper script for Psi4 keywords",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FLongWang/psi4-help",
    packages=find_packages(),
    package_data=package_data,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    install_requires=[
        "PyYAML",
        "colorama"
    ],
    entry_points=entry_points,
)