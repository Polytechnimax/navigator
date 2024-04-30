# `navigator`

## Description

`navigator` is small CLI utility which allows quick access to folders registered by the user.  
It works by keeping a register of name-path pairs and offers various ways of managing this register.

## Why `navigator`?

### Motivation
At some point in my previous job, I had a bunch of projects stored several folders (some in a personal folder, some in my group's svn folder, some in my personal folder of the group svn, some in colleagues folders in the group svn, etc.) 
To quickly navigate to those folders, I designed `navigator`.

### Disclaimer
I do not claim this is the most practical solution or a fantastic utility you should absolutely use... It's just a small script which helped me gain some time and that I still use today. 

## How to install?  
* `make install` will install `navigator` in `/usr/local/lib` and create a symlink in `/usr/local/bin`; it also adds a line in `.zshrc` to enable autocompletion  
* `make uninstall` will uninstall `navigator`, undoing all of the above
* `make full-uninstall` will uninstall `navigator` and remove the register if any exists

## How to use? 

### Intended use
1. You start working on a new project, so you register a name and the path to this project's folder.
2. While working on this project, you can quickly navigate to the project's folder in Terminal and Finder. 
3. You finish working on the project and deregister the name. 

**Note**: You may have several names registered at once.

### Usage

`nav add <name> <path/to/the/folder>`  
registers a new folder; `path` can be absolute or relative.

`nav list`  
lists registered folders  
by default only the *names* of registered folders are displayed; to also display the paths, add option `--path` or `-p`
by default only valid entries (i.e. path are strings that point toward an existing folder) are displayed; to display broken and/or invalid entries add `-a`/`--all` and/or `-b`/`--broken` and/or `-i`/`--invalid`

`nav to <name>`  
navigates with the Terminal to the specified folder  
add `-f`/`--folder` to also open a Finder window at location

`nav del <name>`  
deregisters a folder

`nav clean`
removes broken (i.e. non-existing paths) and invalid (i.e. non-string paths) entries from the register
use `-b`/`--broken` or `-i`/`--invalid` to remove only the broken or invalid ones

## Coming features

I think the current versions is quite nice to use. I'll keep on working on it as I still use it. My current goal is to adapt and turn it into an Alfred Workflow.
