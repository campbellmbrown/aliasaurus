# Aliasaurus

![aliasurus-banner](images/banner.png)

Aliasaurus is a simple Windows app to view, organize, and edit Windows aliases.

## Usage

Simply create a new alias, specifying the name and command:

![image](https://github.com/user-attachments/assets/0ef97555-718f-4e8a-a12f-a3256a66def4)

Then run the new alias:

```shell
>time
Fri 20/12/2024  9:48:39.43
```

### Alias File

On starting the app, Aliasaurus will check that there is a `HKEY_CURRENT_USER\Software\Microsoft\Command Processor\AutoRun` registry key. If it does not exist (or is pointing to a different file), Aliasaurus will create it and set it to `%APPDATA%\aliasarus\alias.cmd`. This file is used to load the aliases into the environment variables when a new command prompt is opened. If the `alias.cmd` file does not exist, Aliasaurus will automatically create it and set it to an empty file.

> [!WARNING]
> If the `AutoRun` registry key already exists but is pointing to a different file, Aliasaurus will overwrite it.

The directory of the alias file (`%APPDATA%\aliasarus`) can be viewed in the File Explorer with the File > Open Alias Directory.

### Viewing, Editing, and Saving Aliases

Aliasaurus will read the `alias.cmd` file and load the aliases into the app. The user can then view, add, edit, and delete aliases. Aliases can have multi-line commands. The aliases are saved to the `alias.cmd` file when:

* An edited alias is saved
* The order of the aliases is changed

### Terminal

A new terminal needs to be opened to use a newly-saved alias. This can be done quickly using Run > Open Terminal or the Open Terminal button in the toolbar. This will open a new Command Prompt window.

### Backup

A backup of the alias file can be created using File -> Create Backup. This will create a timestamped backup file in the `%APPDATA%\aliasarus` directory.
The backup has to be manually restored.

### Theme

There are two themes available: Light and Dark. The theme can be changed in the File > Preferences menu. Your selection is saved to settings and preserved across app sessions.

#### Light Mode

![image](https://github.com/user-attachments/assets/4a6281da-3612-4dee-b735-b4c135542428)

#### Dark Mode

![image](https://github.com/user-attachments/assets/db7c2167-3824-4830-8fe7-9326997f414d)

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
git rev-parse --short=8 HEAD > resources/GIT_SHA
pyinstaller --onefile --noconsole --add-data "resources;resources" --icon=resources/logo.ico aliasaurus.py
```

The executable (``aliasaurus.exe``) will be in the ``dist`` directory.

## Build Installer

Build the installer using Docker:

```bash
docker run --rm -v .:/work amake/innosetup:innosetup6 installer/installer.iss
```
