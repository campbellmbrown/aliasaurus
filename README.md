# Aliasaurus

![aliasurus-banner](images/banner.png)

Aliasaurus is a simple Windows app to view, organize, and edit Windows aliases.

## Usage

On starting the app, Aliasaurus will check that there is a `HKEY_CURRENT_USER\Software\Microsoft\Command Processor\AutoRun` registry key. If it does not exist (or is pointing to a different file), Aliasaurus will create it and set it to `%APPDATA%\aliasarus\alias.cmd`. This file is used to load the aliases into the environment variables when a new command prompt is opened. If the `alias.cmd` file does not exist, Aliasaurus will automatically create it and set it to an empty file.

> [!WARNING]
> If the `AutoRun` registry key already exists but is pointing to a different file, Aliasaurus will overwrite it.

Aliasaurus will read the `alias.cmd` file and load the aliases into the app. The user can then view, add, edit, and delete aliases. Aliases can have multi-line commands. The aliases are saved to the `alias.cmd` file when:

* An edited alias is saved
* The order of the aliases is changed

## Development

### Prerequisites

* Python 3.13.0
* Requirements installed via `pip install -r requirements.txt`
* Docker (for building the installer)

### Running Locally

From the command line:

```bash
python aliasaurus.py
```

The app can alternatively be run in VS Code using the `Aliasaurus` launch configuration or the `run` build task.

### Clean

```bash
rm -rf dist build aliasaurus.spec resources/GIT_SHA installer/*.exe
```

## Build Executable

> [!IMPORTANT]
> Building the executable is done locally for now using Python 3.13.0.

Build into a single executable using PyInstaller:

```bash
sh sh/publish.sh
```

The executable (``aliasaurus.exe``) will be in the ``dist`` directory.

## Build Installer

Build the installer using Docker:

```bash
docker run --rm -v .:/work amake/innosetup:innosetup6 installer/installer.iss
```
