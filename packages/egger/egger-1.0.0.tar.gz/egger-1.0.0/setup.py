from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name="egger",
    version="1.0.0",
    author="Thomas J. Booth",
    author_email="thoboo@biosustain.dtu.dk",
    packages=find_packages(),
    description="a python package for graphing emapper results",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/DrBoothTJ/egger",
    license='GNU General Public License v3.0',
    python_requires='>=3.9',
    install_requires=['matplotlib','plotly','scipy','seaborn','Bio'],
    entry_points={'console_scripts': ["egger=egger.__main__:entrypoint"]}
)
