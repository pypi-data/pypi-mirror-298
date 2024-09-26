from setuptools import find_packages, setup

setup(
    name="mdr_python_api",
    version="1.1.4",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["requests"],
)
