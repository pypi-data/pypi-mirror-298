from setuptools import setup, find_packages

setup(
  name='library_example',
  version='0.2',
  packages=find_packages(),
  install_requires=[
  ],
  entry_points={
     "console_scripts": [
         "library_example = library_example:hello",
     ],
  }
)


