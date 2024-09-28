from setuptools import setup, find_packages

setup(
    name="gibbs-reconstructor",
    version="1.0.1",
    author="Félix Laplante",
    author_email="flheight0@gmail.com",
    description="Gibbs Reconstruction for linear data reconstruction",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/flheight/gibbs-reconstructor-pypi/",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "tqdm",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.8',
)
