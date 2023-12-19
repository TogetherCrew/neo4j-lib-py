from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="tc-neo4j-lib",
    version="1.0.1",
    author="Mohammad Amin Dadgar, TogetherCrew",
    maintainer="Mohammad Amin Dadgar",
    maintainer_email="dadgaramin96@gmail.com",
    packages=find_packages(),
    description="A neo4j shared library to use across togethercrew python projects.",
    long_description=open("README.md").read(),
    install_requires=requirements,
)
