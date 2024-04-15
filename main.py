import os
import shutil
import argparse
import time
import logging
import hashlib

def setup_logging(log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    return hasher.hexdigest()

def sync_folders(source, replica):
    for item in os.listdir(source):
        source_item = os.path.join(source, item)
        replica_item = os.path.join(replica, item)

        if os.path.isdir(source_item):
            if not os.path.exists(replica_item):
                os.makedirs(replica_item)
                logging.info(f"Created directory {replica_item}")
            sync_folders(source_item, replica_item)
        else:
            if not os.path.exists(replica_item) or \
               file_hash(source_item) != file_hash(replica_item):
                shutil.copy2(source_item, replica_item)
                logging.info(f"Copied file {source_item} to {replica_item}")

    for item in os.listdir(replica):
        replica_item = os.path.join(replica, item)
        source_item = os.path.join(source, item)

        if not os.path.exists(source_item):
            if os.path.isdir(replica_item):
                shutil.rmtree(replica_item)
            else:
                os.remove(replica_item)
            logging.info(f"Removed {replica_item}")

def main():
    parser = argparse.ArgumentParser(description="Folder Synchronization Tool")
    parser.add_argument("source", help="Path to source folder")
    parser.add_argument("replica", help="Path to replica folder")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", help="Path to log file")
    args = parser.parse_args()

    setup_logging(args.log_file)

    logging.info("Starting folder synchronization...")
    
    while True:
        try:
            sync_folders(args.source, args.replica)
            logging.info("Folders synchronized successfully.")
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")

        time.sleep(args.interval)

if __name__ == "__main__":
    main()