import re
import sys
import json
import os

DEBUG = False

def debug(str, *args, **kwargs):
    if DEBUG:
        print("debug: " + str, args, kwargs)

class Replacer:
    """Replaces text in files matching patterns."""

    def replace(self, pth: str, target: str, replacement: str, is_regex: bool):
        p = os.path.normpath(pth)
        original = self.__get_text(p)
        text, count = re.subn(target, replacement, original) if is_regex else (
            original.replace(target, replacement), -1)
        self.__write_text(p, text)
        short_path = p.split('\\')[-1]
        if count > -1: 
            print(f"{short_path}: {count} replacements made.")
        else:
            print(f"{short_path}: processing completed. ")

    def __write_text(self, p, text):
        with open(p, mode="w") as fw:
            fw.write(text)

    def __get_text(self, p):
        with open(p, mode="r") as fr:
            return fr.read()

rep = Replacer()
args = iter(sys.argv)
next(args)
for json_path in args:
    with open(json_path, "r") as jf:
        j = json.load(jf)
    for file in j['files']:
        p = file['path']
        debug("file:",p)
        for replacement in file['replacements']:
            regex = False
            if 'pattern' in replacement:
                target = replacement['pattern']
                regex = True
            else:
                target = replacement['target']
            debug("pattern:", target)
            replace_text = replacement['replace']
            debug("replace_text:", replace_text)
            rep.replace(p, target, replace_text, is_regex=regex)
