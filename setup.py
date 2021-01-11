import setuptools
import versioneer

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="firefly-cli",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Afonso Costa",
    description="A python-based command line interface for practically entering expenses in Firefly III",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/afonsoc12/firefly-cli",
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas==1.1.4',
        'requests==2.25.1',
        'tabulate==0.8.7',
        'xdg==5.0.1',
    ],
    entry_points={
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
)