## OP-1 Tools
This is a set of tools I use for the Teenage Engineering OP-1. It was tested on Linux, most likely works on Mac, and no idea about Windows.

### Deduplicator
The deduplicator script finds identical files between a newer and an older backup and replaces the duplicate file with a link to save storage space.

It is recommended to create a copy of the "new" directory on initial run to test out functionality. "New" directory is the only one altered
#### usage:
```
python3 deduplicator.py -p <old_directory_location> -n <new_directory_location> --dry-run
```
Real example, with dry run (will not actually copy):
```
python3 deduplicator.py -p ~/op1_test/2020-03-23-17-45-42/ -n ~/op1_test/2020-04-16-14-11-52/ --dry-run
```
As this script permanently deletes files, it is recommended to run as dry run initially to understand what gets deleted.
#### arguments:
```
-p / --previous : Directory of older directory
-n / --new : Directory of newer directory
--dry-run : Including this flag means it will only do test run, showing which files will be deleted.
```

### op1_backup
This tool uses rsync to backup files off mounted OP-1 to local computer. User needs to edit file to include local storage locations.

### op1_reload
This tool reloads backup from local computer to OP-1. User needs to edit file to include local storage locations.
