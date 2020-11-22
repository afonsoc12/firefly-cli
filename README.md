![](https://www.firefly-iii.org/static/img/logo-small-new.png)

# Firefly III Command Line Interface

A python-based command line interface for practically entering expenses in [Firefly III](https://www.firefly-iii.org).

# Instalation
This program is available on PyPI. So the easiest way to install is:
```shell
# Install firefly-cli from PyPI
pip install firefly-cli

# Enjoy! Runs firefly-cli
firefly-cli
```

Alternatively, you can clone the repository and run the library module as a script:
```shell
# Clone the repository
git clone

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

# Commands
The scope of this CLI is to enter expenses in CSV style. Therefore, some commands do not have a "very polished" UI for the moment. I am looking forward to improve this soon!

If you find any bugs (which you WILL!), please submit a new issue or PR! I am more than happy to accept new suggestions, improvements and corrections.

A summary of the available commands is the following:

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

