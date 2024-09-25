from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="cpykg",
    version="0.0.6",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "cpykg": ["data/*.csv"]
    },
    include_package_data=True,
)