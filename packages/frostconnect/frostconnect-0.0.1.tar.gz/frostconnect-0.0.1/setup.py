import pathlib
import setuptools


setuptools.setup (
    name="frostconnect",
    version="0.0.1",
    description="Small package that has db connection functionality.",
    long_description=pathlib.Path("Readme.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://www.github.com/mk732",
    author="MK732",
    license="The Unlicense",
    python_requires=">=3.9",
    install_requires=["asyncpg", "asyncio", "python-dotenv"],
    packages=setuptools.find_packages(),
    extras_require={
        "dev" : ["pytest>=7.0", "twine>=4.0.2"]
    },
    include_package_data=True,
)