# datascience-for-ek

### Note: all sub-projects should use poetry

### Poetry: Installation

The easiest way to install poetry package manager is to use pipx.
Just follow these commands.

```shell
### 👇 Only once 👇 ###
brew install pipx # Install pipx executor

pipx install poetry # Install poetry.
# Now poetry is installed in an isolated environment in your user folder.
### 👆 Only once 👆 ###
```

### Project: Checkout

```shell
cd <folder name> # Checkout the lab folder
poetry install # Install dependencies
```

### Project: Creation

1. Initialize

```shell
poetry init
# Hit yes yes yes, and just create this pyproject.toml
```

2. Add `package-mode = false` inside `pyproject.toml`.

3. Add dependency

```shell
# This is how you add dependencies.
poetry add numpy
```

4. Enjoy!
