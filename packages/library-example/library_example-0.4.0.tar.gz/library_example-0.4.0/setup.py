from setuptools import setup, find_packages

with open('Readme.md','r') as f:
    description = f.read()

setup(
  name='library_example',
  version='0.4.0',
  packages=find_packages(),
  install_requires=[
  ],
  entry_points={
     "console_scripts": [
         "library_example = library_example:hello",
     ],
  },
long_description=description,
long_description_content_type='text/markdown',
)


