from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="package_name_Alisson_Wendel",
    version="0.0.1",
    author="Alisson",
    description="Pacote para estudo de conceitos de criação de pacotes",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alissonwr/simple-package-template.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.5',
)