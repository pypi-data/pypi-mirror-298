import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="m_pyutil",
    version="1.6.1",
    author="sxydh",
    author_email="sxydhgg@gmail.com",
    description="NOTHING",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sxydh/m-pyutil",
    packages=setuptools.find_packages(),
    install_requires=[
        'pymongo',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
