
from setuptools import setup, find_packages

def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()

setup(
      name="UdemyCalculatorEkene",
      version="2.0.0",
      packages=find_packages(include=['udemyCalculator', 'udemyCalculator.*']),
      install_require=[],
      url="",
      LICENCE="",
      author = "Ekenedirichukwu Obianom",
      description = "This is my first trial on building a package.",
      long_description=read_file(file_name="README.md"),
      python_requires=">= 3.6"
      )