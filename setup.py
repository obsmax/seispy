import setuptools, os
from seispy.version import __version__


with open("Readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seispy",  # Replace with your own username
    version=__version__,
    author="Maximilien Lehujeur",
    author_email="maximilien.lehujeur@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Linux"],
    python_requires='>=3.7',
    scripts=[os.path.join("seispy", "bin", "viz"), ])
