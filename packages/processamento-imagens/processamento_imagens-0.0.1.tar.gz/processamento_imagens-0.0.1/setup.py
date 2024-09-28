from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()
    
with open("requirements.txt") as f:
    requirements = f.read().splitlines()
    
setup(
    name="processamento_imagens",
    version="0.0.1",
    author="ReidnerFausto",
    author_email="reidner.fausto123@gmail.com",
    description="teste de processamento de imagens",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)