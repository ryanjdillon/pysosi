
def utfopen(filename):
    '''Read utf encoded files'''
    import chardet
    import codecs
    import io
    import os

    # Handle file encoding
    bytes = min(32, os.path.getsize(filename))
    raw = open(filename, 'rb').read(bytes)

    if raw.startswith(codecs.BOM_UTF8):
        encoding = 'utf-8-sig'
    else:
        result = chardet.detect(raw)
        encoding = result['encoding']

    return io.open(filename, 'r', encoding=encoding)


def get_n_lines(filename):
    '''Get number of lines by calling bash command wc'''
    import os
    import subprocess

    cmd = 'wc -l {0}'.format(filename)
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout

    return int((output).readlines()[0].split()[0])


def indent_ind(line, indent_char):
    '''Return the index locaitons of indent character in a string'''
    ind = list()
    if line:
        for n, c in enumerate(line):
            if c == indent_char:
                ind.append(n)
            else:
                break
    return ind
