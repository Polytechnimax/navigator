# `navigator`

## Description

`navigator` is a CLI utility which allows to quickly register and navigate to work directories. 

## Why `navigator`?

### Motivation
At some point in my previous job, I had a bunch of projects stored several folders (some in a personal folder, some on group svn folder, some in my personal folder of the group svn, some in colleagues folders in the group svn, etc.) 
To quickly navigate to those folders, I designed `navigator`.

### Disclaimer
I do not claim this is the most practical solution or a fantastic utility you should absolutely use... It's just a small script which helped me gain some time and that I still use today. 

## How to install?  
* `make install` will install `navigator`
* `make uninstall` will uninstall `navigator`
* `make full-uninstall` will uninstall `navigator` and remove the configuration file from home folder.

## How to use? 

### Intended use
1. You start working on a new project, so you register a name an the path to this project's folder.
2. While working on this project, you can quickly navigate to the project's folder in Terminal and Finder. 
3. You finish working on the project and deregister the name. 

**Note**: You may have several names registered at once.

### Usage

`nav add <name> <path/to/the/folder>`  
Registers a new folder. `path` can be absolute or relative.

`nav list`  
Lists registered folders. By default only the *names* of registered folders are displayed; to also display the paths, add option `--path` or `-p`.

`nav to <name>`  
Open terminal and finder window of a registered folder.

`nav del <name>`  
Deregisters a folder. 


## Coming features

I am currently working on (or at least thinking of) adding the following features.  
1. Several small improvements.
2. An installer.
3. An auto-completion system to facilitate navigation.
4. A `doctor` keyword to try and solve corrupted registers.
5. An Alfred Workflow integration.
