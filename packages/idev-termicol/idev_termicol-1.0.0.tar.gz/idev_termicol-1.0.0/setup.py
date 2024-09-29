import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "idev-termicol",
    version = "1.0.0",
    author = "IrtsaDevelopment",
    author_email = "irtsa.development@gmail.com",
    description = "A python Simple python function aimed to handle printing of colored and / or decorated text to console / terminal.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/irtsa-dev/termicol",
    project_urls = {
        "Bug Tracker": "https://github.com/irtsa-dev/termicol/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "idev-termicol"},
    packages = ["termicol"],
    python_requires = ">=3.6"
)