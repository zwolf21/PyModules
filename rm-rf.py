from fnmatch import fnmatch
from argparse import ArgumentParser
from glob import glob
from os import walk, unlink
from os.path import join, abspath

def parse_args():
    parser = ArgumentParser(description="delete file which patterns rm_rf <Dir Path> -p <*.py>, <db.*>....")
    parser.add_argument('files', default='.')
    parser.add_argument('-p', '--patterns', help='-p <file_pattern>', default=['*'], nargs='*')
    parser.add_argument('-v', '--preview', help='-v <file_pattern> pre view before unlink', default=False, action="store_true")

    return parser.parse_args()


def walk_folder(directory, patterns, preview=False):
    matchs = set()

    for cur, dirs, files in walk(directory):
        for f in files:
            for pat in patterns:
                if fnmatch(f, pat):
                    path = join(cur, f)
                    matchs.add(path)

    for path in matchs:
        path = abspath(path)
        print(path) if preview else unlink(path)
            
if __name__ == '__main__':
    args = parse_args()
    walk_folder(args.files, args.patterns, args.preview)
    print(vars(args))