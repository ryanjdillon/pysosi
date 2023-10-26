"""
Read Kartverket SOSI-formatted files to python dictionary
"""

from subprocess import Popen, PIPE
from collections import OrderedDict
from pathlib import Path
from typing import List, Union

from pysosi.utf_utils import utf_open


def read_sos(fp, indent_char="."):
    """
    Read Kartverket SOSI-formatted files to python dictionary

    `NØ` ids are appended with increasing integer IDs. This could be improved,
    but was a quick fix to avoid overwriting existing elements with that ID.

    Parameters
    ----------
    fp: str
        Full path to .sos file being read
    indent_char: str
        Prefix marking heirarchy of elements in .sos file

    Returns
    -------
    data: OrderedDict
        Dictionary of .sos file data with same data heirarchy

    Example
    -------
    >>> from pathlib import Path
    >>> from sosi import read_sos
    >>> data = reas_sos(Path('file.sos'))
    """
    fp = Path(fp)

    # Get number of lines in file for generating progress bar
    n_lines = _get_n_lines(fp)

    # Open file with appropriate encoding
    fh = utf_open(fp)

    # Init counters and key/data containers
    n_id = 0
    level = 0
    keys = [
        "",
    ] * 10
    data = OrderedDict()

    # Read first line for initializing processing loop
    l0 = fh.readline()

    # Read lines until EOF with progress bar
    for i in range(n_lines):
        l1 = fh.readline()

        # Skip divider row(s) beginning with `!`
        if l1.startswith("!"):
            continue

        # Get number of indent characters at start of line
        n0 = len(_get_indent_char_indices(l0, indent_char))
        n1 = len(_get_indent_char_indices(l1, indent_char))

        # Check if line contains indent character
        if n0 > 0:
            # Compare number of indent chars between current and next lines
            # Data line, no heirarchy key present
            if n0 == 0:
                key = _parse_parent(l0[n0:])
                vals = list()
            # Parent line
            elif n0 < n1:
                key = _parse_parent(l0[n0:])
                vals = OrderedDict()
            # Child line with following child line, or
            # Last child line before next parent
            elif (n0 == n1) or (n0 > n1):
                l_list = l0[n0:].replace(":", "").split()
                key = l_list[0]
                vals = l_list[1:]
                vals = vals[0] if len(vals) == 1 else vals

            # Add sequential ID to `NØ` keys to prevent overwrite
            if key == "NØ":
                key = "NØ_{}".format(n_id)
                n_id += 1

            # Set new key for current heirarchy level
            keys[level] = key

        else:
            # Append overlapping single line key/value pairs (e.g. `REF`)
            if l0.startswith(":"):
                vals = vals + l0.replace(":", "").split()[:2]
            # Append data to list of data (e.g. `NØ` collection)
            else:
                vals.append(tuple(val for val in l0.split()[:2]))

        # Assign data to appropriate parent/child dict
        if level == 0:
            data[keys[0]] = vals
        elif level == 1:
            data[keys[0]][keys[1]] = vals
        elif level == 2:
            data[keys[0]][keys[1]][keys[2]] = vals
        else:
            raise SystemError(
                "Implementation supports <=2 levels of nesting. "
                "Current level: {}".format(level)
            )

        # Update level for next iter
        if n1 > 0:
            # Parent line or last child line before next parent
            if (n0 < n1) or (n0 > n1):
                level = n1 - 1

        # Set previous line to current line for next iter
        l0 = l1

    fh.close()

    return data


def _parse_parent(line: str) -> str:
    """
    Parse field key from line
    """
    return line.replace(" ", "_").replace(":", "").strip()


def _get_n_lines(fp: Union[str, Path]) -> int:
    """
    Get number of lines with bash command `wc`
    """

    output = Popen(f"wc -l {fp}", shell=True, stdout=PIPE).stdout

    return int((output).readlines()[0].split()[0])


def _get_indent_char_indices(line: str, indent_char: str) -> List[int]:
    """
    Return the index locations of indent character in a string
    """
    ind = list()
    if line:
        for n, c in enumerate(line):
            if c == indent_char:
                ind.append(n)
            else:
                break
    return ind
