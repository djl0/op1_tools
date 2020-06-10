import os
import sys
import glob
import hashlib
import argparse


TXT_OR_LINK = 'link'

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class Consolidator(object):
    def __init__(self, old_path, new_path, dry_run=False):
        self.new_path = new_path
        self.old_path = old_path
        if self.old_path.endswith('/') and not self.new_path.endswith('/'):
            self.old_path = self.old_path[:-1]
        if not self.old_path.endswith('/') and self.new_path.endswith('/'):
            self.old_path += '/'

        self.dry_run = dry_run

    def dedupe_it(self):
        print("Comparing:")
        print("Old path: ", self.old_path)
        print("New path: ", self.new_path)
        files = glob.glob(self.new_path + '/**/*', recursive=True)
        for f in files:
            if os.path.isfile(f):
                self.check_file(f)

    def check_file(self, file_path):
        new_source_file, new_hash = self.get_source_file_and_hash(file_path)
        old_file_path = file_path.replace(self.new_path, self.old_path)
        old_source_file, old_hash = self.get_source_file_and_hash(file_path)

        # if there is an old file, hashes are the same, and source files aren't already equal:
        if old_hash is not None and new_hash == old_hash and new_source_file != old_source_file:
            if not self.dry_run:
                print('Deleting:', file_path)
                os.remove(file_path)
                # either txt or link option
                if TXT_OR_LINK == 'txt':
                    with open(file_path + '.txt', 'w') as new_dupe_file:
                        new_dupe_file.write(new_hash + '||' + old_source_file + '\n')
                else:
                    os.symlink(old_source_file, file_path)
            else:
                print("Would have deleted: ", file_path)

    @staticmethod
    def get_source_file_and_hash(path):
        original_source = None
        hash = None
        possible_txt_path = path + '.txt'
        if os.path.islink(path):
            original_source = os.path.realpath(path)
            hash = md5(original_source)
        elif os.path.exists(possible_txt_path):
            with open(possible_txt_path, 'r') as hashed_file:
                content = hashed_file.read().strip()
                hash, original_source = content.split('||')
        elif os.path.exists(path):
            hash = md5(path)
            original_source = path
        return original_source, hash


if __name__ == '__main__':
    description = "Tool to consolidate OP-1 backups"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-p", "--previous", help="directory of previous backup", required=True)
    parser.add_argument("-n", "--new", help="directory of newer backup", required=True)
    parser.add_argument('--dry-run', dest='dry_run', action='store_true')
    parser.set_defaults(dry_run=False)
    parsed = parser.parse_args()

    old_path = parsed.previous
    if not old_path.startswith('/'):
        old_path = os.path.realpath(os.path.join(os.getcwd(), old_path))
    new_path = parsed.new
    if not new_path.startswith('/'):
        new_path = os.path.realpath(os.path.join(os.getcwd(), new_path))

    c = Consolidator(old_path, new_path, dry_run=parsed.dry_run)

    c.dedupe_it()
