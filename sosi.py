#!/usr/bin/env python3

import click

@click.command(help='Read Kartverket SOSI-formatted files to python dictionary')

@click.option('--filename', prompt=False,
               help='Full path toe .sos file being read')
@click.option('--indent-char', prompt=False,
              help='prefix marking heirarchy of elements in .sos file')

def __run(filename, indent_char):
    '''Script wrapper for read_sos()'''

    # TODO add conversion to .shp, etc. here
    data = read_sos(filename, indent_char)

    return data


def read_sos(filename, indent_char='.'):
    '''Read Kartverket SOSI-formatted files to python dictionary

    Args
    ----
    filename: str
        full path toe .sos file being read
    indent_char: str
        Prefix marking heirarchy of elements in .sos file

    Returns
    -------
    data: OrderedDict
        Dictionary of .sos file data with same data heirarchy

    Note
    ----
    `NØ` ids are appended with increasing integer IDs. This could be improved,
    but was a quick fix to avoid overwriting existing elements with that ID.

    Example
    -------
    import sosi
    data = sosi.reas_sos('./filename.sos')
    '''
    from collections import OrderedDict
    import tqdm

    import utils

    # Parse function for parent field keys, and for data lines
    parse_parent = lambda s: s.replace(' ', '_').replace(':','').strip()
    parse_data   = lambda s: s

    # Get number of lines in file for generating progress bar
    n_lines = utils.get_n_lines(filename)

    # Open file with appropriate encoding
    f = utils.utfopen(filename)

    # Init counters and key/data containers
    n_id = 0
    level = 0
    keys = ['',]*10
    data = OrderedDict()

    # Read first line for initializing processing loop
    l0 = f.readline()

    # Read lines until EOF with progress bar
    for i in tqdm.tqdm(range(n_lines)):
        l1 = f.readline()

        # Skip divider row(s) beginning with `!`
        if l1.startswith('!'):
            continue

        # Get number of indent characters at start of line
        n0 = len(utils.indent_ind(l0, indent_char))
        n1 = len(utils.indent_ind(l1, indent_char))

        # Check if line contains indent character
        if n0 > 0:

            # Compare number of indent chars between current and next lines
            # Data line, no heirarchy key present
            if n0 == 0:
                key = parse_parent(l0[n0:])
                vals = list()
            # Parent line
            elif n0 < n1:
                key = parse_parent(l0[n0:])
                vals = OrderedDict()
            # Child line with following child line, or
            # Last child line before next parent
            elif (n0 == n1) or (n0 > n1):
                l_list = l0[n0:].replace(':', '').split()
                key = l_list[0]
                vals = l_list[1:]
                vals = vals[0] if len(vals) == 1 else vals

            # Add sequential ID to `NØ` keys to prevent overwrite
            if key == 'NØ':
                key = 'NØ_{}'.format(n_id)
                n_id += 1

            # Set new key for current heirarchy level
            keys[level] = key

        else:
            # Append overlapping single line key/value pairs (e.g. `REF`)
            if l0.startswith(':'):
                vals = vals + l0.replace(':','').split()[:2]
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
            raise SystemError('Implementation supports <=2 levels of nesting. '
                              'Current level: {}'.format(level))

        # Update level for next iter
        if n1 > 0:
            # Parent line or last child line before next parent
            if (n0 < n1) or (n0 > n1):
                level = n1-1

        # Set previous line to current line for next iter
        l0 = l1

    f.close()

    return data


if __name__ == '__main__':
    __read_sos()
