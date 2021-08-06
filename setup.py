"""Setup script to install openident as a package"""

import os

from setuptools import find_namespace_packages, setup
from setuptools.command.develop import develop

BASEPATH = os.path.dirname(os.path.realpath(__file__))

REQUIREMENTS = open(os.path.join(BASEPATH, "requirements.txt")).read().splitlines()
REQUIREMENTS_DEV = (
    open(os.path.join(BASEPATH, "requirements_dev.txt")).read().splitlines()
)


class DevelopCommand(develop):
    """ "Custom develop command that also installs development requirements"""

    def __init__(self, dist, **kw):
        dist.install_requires.extend(REQUIREMENTS_DEV)
        super().__init__(dist)


setup(
    name="openident",
    version="0.0.1",
    url="https://github.com/lennart-k/openident",
    author="Lennart K",
    packages=find_namespace_packages(include=("openident", "openident.*")),
    include_package_data=True,
    install_requires=[REQUIREMENTS],
    cmdclass={"develop": DevelopCommand},
    python_requires=">=3.9.0",
    license="MIT",
    project_urls={
        "GitHub": "https://github.com/lennart-k/openident",
        "Docs": "https://openident.readthedocs.io/en/latest/",
    },
    entry_points={
        "console_scripts": [
            "openident = openident.__main__:main",
        ]
    },
)
