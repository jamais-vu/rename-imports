import os
import re

from typing import List

# Matches import statements from module import which don't end in '.js'.
#
# IMPORTANT:
# This doesn't ignore module names with other extensions! Be careful!

# CONFIG
# You change these options to suit your own workflow.

# `OUTDIR` is the directory where your transpiled `.js` files live.
# This should be the same as the `outDir` setting in your `tsconfig.json`.
OUTDIR: str = 'js'

# `EXCLUDE` is a list of file/directory paths you want to ignore.
EXCLUDE: List[str] = []

# TODO: Add an option for list of modules to ignore, eg 'mocha' or 'chai'.
#       That might make the regex pattern significantly more complex, maybe it
#       would be better to do that with the built-in Python string functions.


def main():
    add_js_extensions_for_dir(OUTDIR)


def add_js_extensions_for_dir(dir_: str, exclude: List[str] = EXCLUDE):
    """Adds '.js' extension to imports lacking it in all files in the dir.

    Parameters:
        dir_ : str
            A directory path.
        exclude : List[str]
            A list of paths, as strings, to ignore.
    """
    os.chdir(dir_)  # We move into the directory
    paths: List[str] = [path for path in os.listdir() if path not in EXCLUDE]
    for path in paths:
        if os.path.isfile(path) and path.endswith('.js'):
            # If it's a js file, we add the extensions to its module imports.
            add_js_extensions_for_file(path)
        else:
            # If it's a directory, we call this function again.
            add_js_extensions_for_dir(path)
            os.chdir('..')  # Move back up after finishing that directory


def add_js_extensions_for_file(file_path: str):
    """Adds '.js' extension to module imports lacking it in the given file.

    Parameters:
        file_path : str
            A .js file with ES6 module imports.
    """
    # First we get the contents of the file as a single string.
    text: str = ''
    with open(file_path, 'r') as fo:
        text = ''.join(fo.readlines())  # Text of file as single string

    # Then we substitute each line which matches the import pattern.
    # Negative lookbehind here ensures 3 chars before "';" are not ".js"
    subbed_text: str = re.sub(
        r"import (?P<imports>.*) from '(?P<module>.*(?<!\.js))';",
        r"import \g<imports> from '\g<module>.js';",
        text)

    # Finally we overwrite the file with the new lines.
    with open(file_path, 'w') as fo:
        fo.write(subbed_text)


if __name__ == '__main__':
    main()
