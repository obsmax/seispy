import setuptools, os

# fuck distutils2
version_file = os.path.join('seispy', 'version.txt')
with open(version_file, "r") as fh:
    __version__ = fh.read().rstrip('\n')

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
    install_requires=[
        'timetools @ git+https://gitlab.com/obsmax/timetools.git@v0.0.2#egg=timetools',
        'numpy', 'scipy', 'matplotlib'],
    scripts=[os.path.join("seispy", "bin", "viz"), ])
