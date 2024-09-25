from setuptools import setup, find_packages


setup(
    name="mc-handler",
    author="1attila",
    version="1.0.0",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"])
)