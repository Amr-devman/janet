import setuptools
import pathlib

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="janet", # Replace with your own username
    version="0.1.4",
    author="Amr Ahmed",
    author_email="amrahmed.business@gmail.com",
    description="Janet: manage your python projects more efficiently",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/veryprofessionalusername/janet",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'colorama',
          'psutil',
          'apscheduler',
          'pyfiglet'
      ],
    python_requires='>=3.6',
)