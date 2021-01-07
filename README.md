![](https://www.firefly-iii.org/static/img/logo-small-new.png)

# Firefly III Command Line Interface
[![PyPi Version](https://img.shields.io/pypi/v/firefly-cli.svg)](https://pypi.org/project/firefly-cli/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A python-based command line interface for practically entering expenses in [Firefly III](https://www.firefly-iii.org).

*This project was inspired on [firefly-bot](https://github.com/vjFaLk/firefly-bot), a Telegram bot to create transactions in Firefly III. Some of the API code and examples were forked from this project.*

# Instalation
This CLI tool is available on PyPI. So the easiest way to install is:
```shell
# Install firefly-cli from PyPI
pip install firefly-cli

# Enjoy! Runs firefly-cli
firefly-cli
```

Alternatively, you can clone the repository and run the library module as a script:
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
  - In one-line command style:
    
```shell
$ firefly-cli add 5.2, Large Mocha, Cash, Starbucks
```
  
  - Command Line Interface:
  
```bash
$ firefly-cli
    
Copyright 2020 Afonso Costa

Licensed under the Apache License, Version 2.0 (the "License");
Type "license" for more information.

Welcome to FireflyIII Command Line Interface!
Created by Afonso Costa (@afonsoc12)

===== Status =====
  - URL: https://firefly.mydomain.com
  - API Token: *****xYcV
  - Connection: OK!

Type "help" to list commands.

🐷 ➜
```

# Setup
If you run firefly-cli, you will see that you do not have connection.
In order to configure your Firefly III `URL` and `API_TOKEN` you have to run these two commands:

```shell
# Start CLI, well this one does not count as a command 🙃
firefly-cli

# Set your Firefly URL, such as https://firefly.mydomain.com
edit URL <YOUR URL>

# Set your Firefly API_TOKEN
edit API_TOKEN <YOUR API TOKEN>
```

After entering these values, firefly-cli will automatically refresh API connection. At any point you can refresh API connection by yourself:
```shell
# Refreshes API connection
refresh
```

# Commands
The scope of this CLI is to enter expenses in a comma-separated style. Therefore, some commands do not have a "very polished" UI for the moment. I am looking forward to improve this soon!

If you find any bugs (which you WILL!), please submit a new issue or PR! I am more than happy to accept new suggestions, improvements and corrections.

Summary of the available commands:

| Command  | Description                                                                                                                |
|----------|----------------------------------------------------------------------------------------------------------------------------|
| `help`     | Shows the available commands.                                                                                              |
| `accounts` | Shows budgets information (UI unpolished).                                                                                  |
| `add`      | Adds a transaction to firefly (See `add` section).                                                              |
| `budgets`  | Shows budgets information (UI unpolished).                                                                                  |
| `edit`     | Edits URL and API_TOKEN parameters. Type edit [URL/API_TOKEN] <VALUE>` to configure firefly-cli with your Firefly instance. |
| `exit`     | Exits the CLI tool.                                                                                                        |
| `help`     | Shows available commands. Type `help [command]` to display information about that command.                                   |
| `license`  | Shows License information.                                                                                                 |
| `refresh`  | Refreshes API connection.                                                                                                  |
## `add`
This command is responsible for entering a new expense in your Firefly instance.
The fields available are: 

| Amount | Description | Source account | Destination account | Category | Budget |
|:------:|:-----------:|:--------------:|:-------------------:|:--------:|:------:|

The first three fields can't be omitted.

**Examples:**
- A simple one:

  - `🐷 ➜ add 5, Large Mocha, Cash`

- One with all the fields being used:
 
  - `🐷 ➜ add 5, Large Mocha, Cash, Starbucks, Coffee Category, Food Budget`

- You can skip specfic fields by leaving them empty (except the first two):
  - `🐷 ➜ add 5, Large Mocha, Cash, , , UCO Bank` 

