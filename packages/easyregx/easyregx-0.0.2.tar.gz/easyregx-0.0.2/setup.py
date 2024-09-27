import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easyregx",
    version="0.0.2",
    author="Balakrishnan",
    author_email="admin@reccebird.com",
    description="This python tool help to regex code easier",
    long_description="Added wordsearch function",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/easyregx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)