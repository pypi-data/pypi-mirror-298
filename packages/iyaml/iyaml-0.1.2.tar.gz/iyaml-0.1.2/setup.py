from distutils.core import setup
import io
import os


def read(*paths, **kwargs):
    content = ""
    path = os.path.join(os.path.dirname(__file__), *paths)
    encoding = kwargs.get("encoding", "UTF-8")
    with io.open(path, encoding=encoding) as file:
        content = file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="iyaml",
    version=read("VERSION"),
    description="YAML macro processor",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Andrey Melnikov",
    author_email="andmeln@hotmail.com",
    url="https://github.com/andmeln/iyaml/",
    license="Apache License, Version 2.0",
    packages=["iyaml"],
    install_requires=read_requirements("requirements.txt"),
    python_requires=">=3.7",
)
