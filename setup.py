from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in gad_management/__init__.py
from gad_management import __version__ as version

setup(
	name="gad_management",
	version=version,
	description="Ecuadorian Gads App Management",
	author="Luis Pillaga",
	author_email="lpillaga@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
