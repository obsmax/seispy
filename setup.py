import setuptools, os

# fuck distutils2
version_file = os.path.join('seispy', 'version.py')
if not os.path.isfile(version_file):
    raise IOError(version_file)

with open(version_file, "r") as fid:
    for l in fid:
        if l.strip('\n').strip().startswith('__version__'):
            __version__ = l.strip('\n').split('=')[-1].split()[0].strip()
            break
    else:
        raise Exception(f'could not detect __version__ affectation in {version_file}')

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
        'timetools @ git+https://gitlab.com/obsmax/timetools.git@v0.0.3#egg=timetools',
        'numpy', 'scipy', 'matplotlib'],
    scripts=[os.path.join("seispy", "bin", "viz"), ])
