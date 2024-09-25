from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="dados_moeda",
    version="0.0.1",
    author="Rodrigo França",
    author_email="rodrigo_franca92@hotmail.com",
    description="Data conversion",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rodrigo1708/dados_moeda.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)