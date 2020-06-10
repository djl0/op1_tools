import os
import sys
import glob
import hashlib


TXT_OR_LINK = 'link'

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class Consolidator(object):
    def __init__(self, old_path, new_path):
        self.new_path = new_path
        self.old_path = old_path
        if self.old_path.endswith('/') and not self.new_path.endswith('/'):
            self.old_path = self.old_path[:-1]
        if not self.old_path.endswith('/') and self.new_path.endswith('/'):
            self.old_path += '/'

    def do_it(self):
        files = glob.glob(self.new_path + '/**/*', recursive=True)
        for f in files:
            if os.path.isfile(f):
                self.check_file(f)

    def check_file(self, file_path):
        new_hash = md5(file_path)
        old_file_path = file_path.replace(self.new_path, self.old_path)
        old_hash = None
        prev_file = None
        # either txt or symlink
        # if old file is hash txt file...
        already_hashed_path = old_file_path + '.txt'
        if os.path.exists(already_hashed_path):
            with open(already_hashed_path, 'r') as old_hashed_file:
                content = old_hashed_file.read().strip()
                old_hash, prev_file = content.split('||')
        elif os.path.islink(old_file_path):
            prev_file = os.path.realpath(old_file_path)
            old_hash = md5(prev_file)
        if old_hash is None and os.path.exists(old_file_path):
            old_hash = md5(old_file_path)

        if old_hash is not None and new_hash == old_hash:
            if prev_file is None:
                prev_file = old_file_path
            print('deleting:', file_path)
            os.remove(file_path)
            # either txt or link option
            if TXT_OR_LINK == 'txt':
                with open(file_path + '.txt', 'w') as new_dupe_file:
                    new_dupe_file.write(new_hash + '||' + prev_file + '\n')
            else:
                os.symlink(prev_file, file_path)

if __name__ == '__main__':
    old_path = sys.argv[1]
    if not old_path.startswith('/'):
        old_path = os.path.realpath(os.path.join(os.getcwd(), old_path))
    new_path = sys.argv[2]
    if not new_path.startswith('/'):
        new_path = os.path.realpath(os.path.join(os.getcwd(), new_path))

    c = Consolidator(old_path, new_path)

    c.do_it()
