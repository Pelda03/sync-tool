# Folder Synchronization Tool

This Python script synchronizes the contents of a source folder to a replica folder. It's useful for creating backups of important files or keeping multiple directories in sync.

## Features

- Recursively copies all files and subdirectories from the source to the replica.
- Uses MD5 hashing to check if a file has changed before copying it.
- Logs all actions to a specified log file.
- Can be set to run continuously, checking for changes at a specified interval.

## Usage

You can run the script from the command line using the Python interpreter. You need to provide the source folder, replica folder, synchronization interval (in seconds), and log file path as command-line arguments. Here's an example:

```bash
python main.py "path_to_source_folder" "path_to_replica_folder" 60 log.txt
```