import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'inflect>=2.1.0',
    'Werkzeug>=0.14.1'
]

setuptools.setup(
    name="Hako",
    version="0.0.1",
    author="Austen Cameron",
    author_email="austen.cameron@gmail.com",
    description="A simple python web framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gohako/framework",
    packages=setuptools.find_packages(),
    install_requires = requirements,
    test_require= requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
