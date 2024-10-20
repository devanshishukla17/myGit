import argparse
import sys
from pathlib import PurePath
from pathlib import Path
import textwrap

from . import base
from .data import MyGitFuncs
from .base import MyGitHigherFuncs
import hashlib


def parse_args():
    parser = argparse.ArgumentParser(
        description="A simple Git-like version control system"
    )
    commands = parser.add_subparsers(dest="command")
    commands.required = True

    init_parser = commands.add_parser("init", help="Initialize a new repository")
    init_parser.set_defaults(func=init)

    hash_object_parser = commands.add_parser(
        "hash-object", help="Compute object ID and optionally create a blob from a file"
    )
    hash_object_parser.set_defaults(func=hash_object)
    hash_object_parser.add_argument("file", help="File to hash")
    hash_object_parser.add_argument("-w",action="store_true")

    cat_file_parser = commands.add_parser(
        "cat-file", help="Provide content of repository object"
    )
    cat_file_parser.set_defaults(func=cat_file)
    cat_file_parser.add_argument("object", help="The object to display")

    write_tree_parser = commands.add_parser("write-tree")
    write_tree_parser.set_defaults(func=write_tree)

    read_tree_parser = commands.add_parser("read-tree")
    read_tree_parser.set_defaults(func=read_tree)
    read_tree_parser.add_argument("tree")

    commit_parser = commands.add_parser("commit")
    commit_parser.set_defaults(func=commit)
    commit_parser.add_argument("-m", "--message", required=True)

    log_parser = commands.add_parser("log")
    log_parser.set_defaults(func=log)
    log_parser.add_argument("oid", nargs="?")

    checkout_parser = commands.add_parser("checkout")
    checkout_parser.set_defaults(func=checkout)
    checkout_parser.add_argument("oid")

    tag_parser = commands.add_parser("tag")
    tag_parser.set_defaults(func=tag)
    tag_parser.add_argument("name")
    tag_parser.add_argument("oid", nargs="?")

    return parser.parse_args()


def init(args):
    try:
        repo_funcs.init()
        print(
            f"Initialized an empty mygit repository in {Path.cwd() / repo_funcs.GIT_DIR}"
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def hash_object(args):
    # try:
    with open(args.file, "rb") as f:
        content = f.read()
        print(repo_funcs.hash_object(content))
    # except FileNotFoundError:
    #     print(f"Error: File '{args.file}' not found", file=sys.stderr)
    #     sys.exit(1)
    # except Exception as e:
    #     print(f"Error: {e}", file=sys.stderr)
    #     sys.exit(1)

#new hash function
'''
def hash_object(args):
    #try:
        with open(args.file, "rb") as f:
            content = f.read()

            if args.algo == 'sha256':
                hash_value = hashlib.sha256(content).hexdigest()
            print(hash_value)
'''

def hash_object(args):
    with open(args.file,'rb') as f:
        content=f.read()
        if args.w == True:
            hash_value = hashlib.sha256(content).hexdigest()
        else:
            hash_value
        print(hash_value)
    


def cat_file(args):
    try:
        sys.stdout.flush()
        sys.stdout.buffer.write(repo_funcs.get_object(args.object, expected=None))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def write_tree(args):
    print(hl_funcs.write_tree())


def read_tree(args):
    hl_funcs.read_tree(args.tree)


def commit(args):
    print(hl_funcs.commit(args.message))


def log(args):
    oid = args.oid or repo_funcs.get_ref("HEAD")
    while oid:
        commit = hl_funcs.get_commit(oid)
        print(f"commit {oid}\n")
        print(textwrap.indent(commit.message, "\t"))
        print("")
        oid = commit.parent


def checkout(args):
    hl_funcs.checkout(args.oid)


def tag(args):
    oid = args.oid or repo_funcs.get_ref("HEAD")
    hl_funcs.create_tag(args.name, oid)


def main():
    global repo_funcs
    repo_funcs = MyGitFuncs()
    global hl_funcs
    hl_funcs = MyGitHigherFuncs()
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
