# Changelog

All notable changes to this project will be documented in this file.

## v0.1.2 (2022-02-28)

### New
- Docker Image
- Full compatibility with endpoint [`POST /api/v1/transactions`](https://api-docs.firefly-iii.org/#/transactions/storeTransaction) using positional arguments (e.g. `--foreign-currency-code GBP` or `--foreign-amount 10.23`)
- Transactions are now processed with argparse for broader compatibility
- Support for "withdraw", "deposit" and "transfer" transaction types
- Allows specifying arbitrary date or datetime for a transaction, respectively using the arguments `--date` or `--datetime` (#6)
- Support for specifying config file LOCATION using the environment variable `FIREFLY_CLI_CONFIG`
- Added colour to certain CLI prints
- Unit testing
- Codebase is now [black](https://black.readthedocs.io/en/stable/) and [isort](https://pypi.org/project/isort/) compliant

### Changed
- CLI engine migrated to [cmd2](https://cmd2.readthedocs.io/en/stable/)
- Command line and entrypoint refactored
- Bumped versioneer
- Fixed bug where budgets and transactions would not be created (#9)

### Removed
- pandas library dependency

## v0.0.10 (2021-04-05)

### Changed
- CI migrated from TravisCI to Github Actions
- Housekeeping

## v0.0.9 (2021-01-11)

### Changed
- Fixed dependencies
- Fixed PyPI release bug
- Fixed tagging issue

## v0.0.5 (2021-01-11)

### Added

- CLI now displays version number

### Changed
- Versioneer properly display version on released packages (PyPI)

## v0.0.4 (2021-01-10)

### Added

- Support for Travis CI build
- Versioneer installed

### Changed

- Configuration file is now a `.ini` and stored at $XDG_CONFIG_HOME/firefly-cli/firefly-cli.ini`

## v0.0.3 (2020-11-22)

### Added

- First release of firefly-cli!
