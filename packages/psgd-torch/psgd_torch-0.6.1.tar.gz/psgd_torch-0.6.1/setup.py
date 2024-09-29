from setuptools import setup, find_packages
# use readme.md as long_description
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="psgd_torch",
    version="0.6.1",
    packages=find_packages(),
    package_data={'psgd_torch': ['*.py']},
    install_requires=[
        "torch",
        "opt_einsum",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)