#!/usr/bin/env python3

import click

@click.command(help='Read Kartverket SOSI-formatted files to python dictionary')

@click.option('--filename', prompt=False,
               help='Full path toe .sos file being read')
@click.option('--indent-char', prompt=False,
              help='prefix marking heirarchy of elements in .sos file')

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

    # TODO generalize for 3+ levels, hdf5 for data assign
    # TODO generalize for duplicate keys
    # TODO init keys list with appropriate # keys

    n_lines = utils.get_n_lines(filename)

    f = utils.utfopen(filename)

    # Assign top header row
    level = 0
    keys = ['',]*10
    data = OrderedDict()
    l0 = f.readline()
    n_id = 0
    for i in tqdm.tqdm(range(n_lines)):
        l1 = f.readline()

        # skip divider
        if l1.startswith('!'):
            continue

        n0 = len(utils.indent_ind(l0, indent_char))
        n1 = len(utils.indent_ind(l1, indent_char))

        # Check if line contains indent character
        if n0 > 0:

            # Compart n indent chars between previous and current lines
            if n0 == 0:
                key = l0[n0:].replace(' ', '_').replace(':','').strip()
                vals = list()
            elif n0 < n1:
                key = l0[n0:].replace(' ', '_').replace(':','').strip()
                vals = OrderedDict()
            elif (n0 == n1) or (n0 > n1):
                l_list = l0[n0:].split()
                key = l_list[0]
                vals = l_list[1:]
                vals = vals[0] if len(vals) == 1 else vals

            if key == 'NØ':
                key = 'NØ_{}'.format(n_id)
                n_id += 1

            keys[level] = key

        else:
            vals.append(tuple(val for val in l0.split()[:2]))

        # Assign data
        if level == 0:
            data[keys[0]] = vals
        elif level == 1:
            data[keys[0]][keys[1]] = vals
        elif level == 2:
            data[keys[0]][keys[1]][keys[2]] = vals
        else:
            raise SystemError('Implementation supports <=2 levels of nesting. '
                              'Current level: {}.'format(level))

        # Update level for next iter
        if n1 > 0:
            vals = None
            if n0 < n1:
                level = n1-1
            elif n0 == n1:
                #keys.pop()
                pass
            elif n0 > n1:
                level = n1-1
                #for _ in range(n1):
                #    keys.pop()

        # Set previous line to current line for next iter
        l0 = l1

    f.close()

    return data


if __name__ == '__main__':
    read_sos()
