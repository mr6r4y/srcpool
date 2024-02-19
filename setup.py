import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    line.strip()
    for line in open("requirements.txt", "r")
    if line.strip() and not line.startswith("-e") and not line.startswith("#")
]


setuptools.setup(
    name="srcpool",
    version="0.1.0",
    author="mr6r4y",
    description="Source pool management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mr6r4y/srcpool",
    package_dir={"": "src/python"},
    packages=setuptools.find_packages("src/python"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "srcpool=srcpool.entrypoints:srcpool",
        ]
    },
)
