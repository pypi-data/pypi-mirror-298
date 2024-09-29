from setuptools import setup, find_packages

setup(
    name="echowave",
    version="0.1.1",
    author="Torrez Tsoi",
    author_email="that1.stinkyarmpits@gmail.com",
    description="A cloned version of the IceCream package that replaces print() with ic() when debugging.",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        # Add your dependencies here, for example:
        # "requests",
    ],
    include_package_data=True,
)
