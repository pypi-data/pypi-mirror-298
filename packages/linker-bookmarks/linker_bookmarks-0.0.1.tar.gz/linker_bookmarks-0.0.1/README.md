# LINKER: cli based bookmark manager #

### Installation

```sh
pipx install linker-bookmarks
pipx ensurepath
```

Ensure you use ```pipx``` to install globally without polluting your system-wide packages.

### Description

*linker* is a tag-based CLI bookmark manager. Quickly and easily save and launch URLs. Linker is designed to be lightweight and small in size, allowing you to easily sync your bookmarks between devices, (eg github, bitbucket, onedrive, etc).

Bookmarks will be saved to $HOME/linker/

Consider converting $HOME/linker into a repository post install.

### Usage

Type ```linker``` to launch.

### Tips

 - Running ```linker``` for the first time will create all necessary files in ```~/linker/```, otherwise linker will use existing files from any previous installs.

 - Config file location is set to ```~/linker/conf/linker.conf```

 - When executing ```linker```, it has its own menu system. However you can incorporate linker into your own scripts using command line options if you wish. EG: ```linker -c "https://github.com/monotone-the-musical/linker" github,example-tag --title "Linker - CLI Based Bookmark Manager"```. It is recommended first time users run this command to populate their empty linker database with a record.

 - Consider having linker as a keyboard shortcut launching a customised terminal session. For example, map ```CTRL+SHIFT+L``` to ```alacritty --config-file /home/mtmuser/.config/alacritty/alacritty.toml.linker -e linker```, where ```alacritty.toml.linker``` is a customised [alacritty](https://github.com/alacritty/alacritty) profile specifically for linker.

### Dependencies

Dependencies will be installed as part of pipx installation above.

 - configparser
 - iterfzf
 - pick
 - pyperclip
 - python-dateutil

