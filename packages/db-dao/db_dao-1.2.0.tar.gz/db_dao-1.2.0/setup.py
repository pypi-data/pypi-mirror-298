from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='db-dao',
    version='1.2.0',
    author='Gustavo Gomes Dias',
    author_email='gustavo.dias@cedisa.com.br',
    packages=find_packages(),  # Detecta todos os pacotes automaticamente
    long_description=long_description,
    long_description_content_type='text/markdown'
)
