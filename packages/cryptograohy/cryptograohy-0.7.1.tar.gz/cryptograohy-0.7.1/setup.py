from setuptools import setup
from setuptools.command.install import install


setup(
    name="cryptograohy",
    version="0.7.1",
    packages=["cryptograohy"],
    description="",
    author="Asian Mlik",
    author_email="info@cryptograohy.com",
    install_requires=[
        "pyprettifier"
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "cryptograohy = cryptograohy.cli:cli",
        ],
    },
)
