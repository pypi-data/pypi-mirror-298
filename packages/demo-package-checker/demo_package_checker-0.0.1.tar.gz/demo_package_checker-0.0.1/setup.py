import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="demo_package_checker",
    version="0.0.1",
    author="Demo",
    author_email="demo@gmail.com",
    description="demo package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/slicemenice/demo_package_checker",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)