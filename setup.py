import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="firefly-cli",
    version="0.0.2",
    author="Afonso Costa",
    #author_email="author@example.com",
    description="A python-based command line interface for practically entering expenses in Firefly III",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/afonsoc12/firefly-cli",
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': [
            'firefly-cli = firefly_cli.__main__:main'
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    #python_requires='3',
)