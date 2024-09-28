# Python Project Manager

This project aims to provide a simple tool for managing Python projects efficiently. Whether you are a beginner or an experienced developer, this tool will help you streamline your workflow and keep your projects organized.

## Available Commands

Here is a list of available commands for the Python Project Manager:

- `init`: Initialize a new Python project.
    - `<project_name> (str)`: The name of the project.
    - `--froce, -f`: Force the initialization project, even if the directory is not empty.
- `install`: Install project dependencies.
    - `args`: Uses pip to install packages in the virtual environment. Args will be passed directly to pip.
    - `--dev, -d`: Adds the dependencies to the `requirements-dev.txt` instead of `requirements.txt`.
    - `--not_required, -n`: Dependencies are not added to either `requirements.txt` or `requirements-dev.txt`.
- `list`: List all current installed dependencies.
    - No arguments.
- `run`: Run scripts defined in the `scripts` section of the `.proj.config` file.
    - `<script_name>`: The name of the script located in the `scripts` section of the `.proj.config` file.
    - `--local, -l`: Run the script in the local environment NOT in the virtual environment.
    - `--python, -p`: Run as a Python script or file.
- `venv`: Manage the virtual environment for the project.
    - `--reset, -r`: Reinitalize the virtual environment.
    - `--install, -i`: Installs dependencies in the virtual environment after initialization.
- `version`: Manage the project version.
    - `<actions>`: The action to perform on the project version. ['inc', 'show', 'set'] default: 'show'.
    - `--major, -M`: Major version.
    - `--minor, -m`: Minor version.
    - `--patch, -p`: Patch version.
    - `--alpha, -a`: Alpha version.
    - `--beta, -b`: Beta version.
    - `--rc, -r`: Release Candidate version.
    - `--local, -l`: Local version.
    - `--timestamp, -t`: Preset: ad the current timestamp to the local version.

Each command comes with its own set of options and arguments. Use `--help` with any command to see more details.

## Initialize a New Python Project

To initialize a new Python project, run the following command:

```ppm init <project_name>```

## Installing and Managing Packages and Dependencies

`ppp install` uses pip as a backend to install packages in the virtual environment. Any arguments passed to `ppm install` will be passed directly to pip unless its one of the specific options for `ppm install`.

#### Installing a Package

To install a package, run the following command:

```ppm install <package_name> [, <package_name> ...]```

#### Listing Installed Packages

To list all installed packages, run the following command:

```ppm list```

Installed packages will be added to the `requirements.txt` file unless the `--dev` or `--not_required` options are used.

#### Installing Dependencies

To install dependencies from a `requirements.txt` and `requirements-dev.txt` file, run the following command:

```ppm install```

#### Pip not found

If you encounter an error saying `pip` is not found, you can use the following command to install it:

```ppm install pip```

## Scripts

You can define custom scripts in the `.proj.config` file under the `scripts` section. These scripts can be run using the `ppm run` command.

`ppm run` will execute the script in the virtual environment unless the `--local` option is used. It can also run Python scripts or files using the `--python` option.

#### Referencing Values

You can reference values from the `.proj.config` useing the following syntax: `%{dot.key}%`.

PPM will dot walk the keys to find the value. If the value is not found.

```json
{
    "src_dir": "path/to/src",
    "test_dir": "path/to/test",
    "test_files": {
        "file1": "test_file1"
    },
    "scripts": {
        "start": "python %src_dir%/main.py",
        "test": "python %test_dir%/%test_files.file1%.py"
    }
}
```

PPM will replace `%src_dir%` with `path/to/src` and `%test_dir%` with `path/to/test`. It will also replace `%test_files.file1%` with `test_file1`.

```
{
    "src_dir": "path/to/src",
    "test_dir": "path/to/test",
    "test_files": {
        "file1": "test_file1"
    },
    "scripts": {
        "start": "python path/to/src/main.py",
        "test": "python path/to/test/test_file1.py"
    }
}
```

You can also use `%env:dot.key%` to reference environment variables. PPM will look for the environment variable in a `.env` file in the project root directory.