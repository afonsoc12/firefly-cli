import setuptools

import versioneer

setuptools.setup(
    name="firefly-cli",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Afonso Costa",
    description="A python-based command line interface for practically entering expenses in Firefly III",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/afonsoc12/firefly-cli",
    packages=setuptools.find_packages(),
    install_requires=[
        "cmd2>=2.4.1,<3",
        "requests-cache>=0.9.4,<1",
        "tabulate>=0.8.9,<1",
        "pyxdg>=0.28,<1",
    ],
    entry_points={"console_scripts": ["firefly-cli = firefly_cli:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    license='Apache-2.0 license',
    license_files='LICENSE'
)
