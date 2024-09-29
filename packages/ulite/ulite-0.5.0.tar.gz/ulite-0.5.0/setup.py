import setuptools
import os

name = 'ulite'

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

here = os.path.abspath(os.path.dirname(__file__))


about = {}
with open(os.path.join(here, name, 'version.py')) as f:
    exec(f.read(), about)

setuptools.setup(
  name=name,
  version=about['__version__'],
  python_requires=">=3.8",
  author="zlols",
  author_email="zlols@foxmail.com",
  description="A GUI module for pygame Community Edition with CSS friendly layout",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://gitee.com/zlols/ulite.py.git",
  py_modules=[name],
  install_requires=[
        'pygame-ce'
    ],
  # packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3 :: Only",
  "License :: OSI Approved :: MIT License",
  # "Operating System :: OS Independent",
  ],
)
