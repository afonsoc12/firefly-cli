<img src="https://www.firefly-iii.org/assets/logo/color.png" width="150">

# Firefly III Command Line Interface
[![PyPi Version](https://img.shields.io/pypi/v/firefly-cli.svg)](https://pypi.org/project/firefly-cli/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
<!-- [![Docker Pulls](https://img.shields.io/docker/pulls/afonsoc12/firefly-cli?logo=docker)](https://hub.docker.com/repository/docker/afonsoc12/firefly-cli) -->

[![Github Starts](https://img.shields.io/github/stars/afonsoc12/firefly-cli?logo=github)](https://github.com/afonsoc12/firefly-cli)
[![Github Fork](https://img.shields.io/github/forks/afonsoc12/firefly-cli?logo=github)](https://github.com/afonsoc12/firefly-cli)
[![Github Release](https://img.shields.io/github/v/release/afonsoc12/firefly-cli?logo=github)](https://github.com/afonsoc12/firefly-cli/releases)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A python-based command line interface for conveniently entering expenses in [Firefly III](https://www.firefly-iii.org).

# Instalation

This CLI tool is available on PyPI and as a docker image.

## 1. Install from PyPI
```shell
# Install firefly-cli from PyPI
pip install firefly-cli

# Enjoy! Runs firefly-cli
firefly-cli
```

## 2. Docker Image
Currently, there are images for both `x86-64` and `arm64` architectures. 

They are built from python's Linux Alpine base image (`python:3.7-alpine`) which makes the application very slim (less than 20MB). 

| Architecture<br>[![Docker Image Size](https://img.shields.io/docker/image-size/afonsoc12/firefly-cli/latest?logo=docker)](https://hub.docker.com/repository/docker/afonsoc12/firefly-cli/tags?page=1&ordering=last_updated&name=latest) | Tag<br>[![Docker Dev Version](https://img.shields.io/docker/v/afonsoc12/firefly-cli/latest?logo=docker)](https://hub.docker.com/repository/docker/afonsoc12/firefly-cli/tags?page=1&ordering=last_updated&name=latest) |
|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|                                                                                                                    x86-64                                                                                                                     |                                                                                                         latest                                                                                                         |
|                                                                                                                     arm64                                                                                                                     |                                                                                                         latest                                                                                                         |

There are also development images with the latest on master branch:

| Architecture<br>[![Docker Image Size](https://img.shields.io/docker/image-size/afonsoc12/firefly-cli/latest?logo=docker)](https://hub.docker.com/repository/docker/afonsoc12/firefly-cli/tags?page=1&ordering=last_updated&name=dev-latest) | Tag<br>[![Docker Dev Version](https://img.shields.io/docker/v/afonsoc12/firefly-cli/dev-latest?logo=docker)](https://hub.docker.com/repository/docker/afonsoc12/firefly-cli/tags?page=1&ordering=last_updated&name=dev-latest) |
|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|                                                                                                                   x86-64                                                                                                                    |                                                                                                               dev-latest                                                                                                               |
|                                                                                                                    arm64                                                                                                                    |                                                                                                               dev-latest                                                                                                               |

Getting started with firefly-cli Docker:
```shell
# Pull latest image
docker pull afonsoc12/firefly-cli:latest

# Test if it is working, mount path to your firefly-cli config folder
docker run --rm -it \
           -v ~/.config/firefly-cli:/config/firefly-cli \
           afonsoc12/firefly-cli:latest

# Set an alias on your .bashrc or .zshrc, so that it is more convenient to run
alias firefly-cli="docker run --rm -it -v ~/.config/firefly-cli:/config/firefly-cli afonsoc12/firefly-cli:latest"

# Add some transactions!
firefly-cli add 5, Large Mocha, Cash, Starbucks
```
## 3. Bare Python
Alternatively, you can clone the repository and install from `setup.py` or run as a python module.

From setup.py:

```shell
# Clone the repository
git clone https://github.com/afonsoc12/firefly-cli.git

# Go to root directory
cd firefly-cli

# Install firefly-cli
pip install .

# Run firefly-cli
firefly-cli
```

Python module:

```shell
# Clone the repository
git clone https://github.com/afonsoc12/firefly-cli.git

# Go to root directory
cd firefly-cli

# Install dependencies
pip install -r requirements.txt

# Run module as a script
python -m firefly_cli
```

# Usage
The CLI has two modes of operation:

1. In one-line command style:
    
```shell
$ firefly-cli add 5.2, Large Mocha, Cash, Starbucks
```
  
2. Command Line Interface:
  
```bash
$ firefly-cli

Copyright 2022 Afonso Costa

Licensed under the Apache License, Version 2.0 (the "License");
Type "license" for more information.

Welcome to FireflyIII Command Line Interface!
Created by Afonso Costa (@afonsoc12)

=============== Status ===============
  - URL: https://firefly.mydomain.com
  - API Token: *****iUcHo
  - Connection: OK!
  - Version: 0.1.0
======================================

Type "help" to list commands.

🐷 ➜
```

# Setup
If you run firefly-cli straight away, a warning will pop up since you haven't configured it with your FireflyIII instance.

In order to configure your Firefly III `URL` and `API_TOKEN` you have to run these two commands (you can find [here](https://docs.firefly-iii.org/firefly-iii/api/#personal-access-token) how to get your API **Personal Access Token**:

```shell
# Start CLI, well this one does not count as a command 🙃
firefly-cli

# Set your Firefly URL, such as https://firefly.mydomain.com
🐷 ➜ edit URL <YOUR URL>

# Set your Firefly API_TOKEN
🐷 ➜ edit API_TOKEN <YOUR API TOKEN>
```

After entering these values, firefly-cli will automatically refresh API connection. At any point, you can trigger a connection refresh:

```shell
# Refreshes API connection
🐷 ➜ refresh
```

Alternatively, you can create a `firefly-cli.ini` file and place it in `$XDG_CONFIG_HOME/firefly-cli/firefly-cli.ini` with the following content:
```yaml
[API]
url = https://firefly.yourdomain.com
api_token = eyXXX
```
**Note:** If `$XDG_CONFIG_HOME` is not set, it defaults to `$HOME/.config/firefly-cli/firefly-cli.ini`

firefly-cli can override this behaviour and read/write from the file specified by the environment variable `FIREFLY_CLI_CONFIG`.

# Commands
The scope of this CLI is to enter expenses in a comma-separated style. 

Starting in **[v0.1.0](https://github.com/afonsoc12/firefly-cli/releases/tag/v0.1.0)**, it now supports adding all possible transaction fields using optional arguments (e.g. `--source-name "Bank HSBC"`). 
The comma-separated arguments (aka positional arguments) are maintained for backwards-compatibility, but optional arguments will **always** override the comma-separated ones

Summary of the available commands:

| Command         | Description                                                                                                                 |
|-----------------|-----------------------------------------------------------------------------------------------------------------------------|
| `help`          | Shows the available commands.                                                                                               |
| `accounts`      | Shows budgets information (UI unpolished).                                                                                  |
| `add`           | Adds a transaction to FireflyIII (See `add` section).                                                                       |
| `budgets`       | Shows budgets information (UI unpolished).                                                                                  |
| `edit`          | Edits URL and API_TOKEN parameters. Type edit [URL/API_TOKEN] <VALUE>` to configure firefly-cli with your Firefly instance. |
| `exit`          | Exits the CLI tool.                                                                                                         |
| `help`          | Shows available commands. Type `help [command]` to display information about that command.                                  |
| `license`       | Shows License information.                                                                                                  |
| `refresh`       | Refreshes API connection.                                                                                                   |
| `version` | Shows firefly-cli version.                                                                                                  |

## Adding a transaction
The command `add` is responsible for entering a new transaction in your Firefly instance. Further help can be shown by typing `add --help` or `help add`.

By default, every transaction is a **withdrawal** and is placed with the current date and time. 
You may change transaction type by including the optional argument `--type`, change the transaction date with `--date yyyy-mm-dd` or if you would like to be more precise `--datetime yyyy-mm-ddTHH:MM:SS`.

The comma-separated fields available are the following:

`Amount, Description , Source account, Destination account, Category, Budget `

**The first four fields can NEVER be omitted!**

### Examples

```shell
# These four fields are mandatory
# Mandatory fields: amount, description, source_account, destination_account
🐷 ➜ add 5, Large Mocha, Cash, Starbucks

# Don't need to be exclusively comma-separated fields, as long as they are specified
🐷 ➜ add --amount 5 --description "Large Mocha" --source-name Cash --destination-name Starbucks

# Or a mixture of comma-separated and optional arguments
🐷 ➜ add 5, Large Mocha --source-name Cash --destination-name Starbucks

# Remember: optional arguments ALWAYS override comma-separated ones
🐷 ➜ add 5, Large Mocha, Cash, Starbucks --source-name "Bank HSBC"
# will create a transaction whose source is "Bank HSBC" and NOT "Cash"

# You can skip specfic fields by leaving them empty
🐷 ➜ add 5, Large Mocha, Cash, Starbucks, , Morning Coffees
# sets the budget to "Morning Coffees" and skips the category
```

## Credits

Copyright 2022 Afonso Costa

Licensed under the [Apache License, Version 2.0](https://github.com/afonsoc12/firefly-cli/blob/master/LICENSE) (the "License")

FireflyIII logo extracted from the official [FireflyIII website](https://www.firefly-iii.org/)
