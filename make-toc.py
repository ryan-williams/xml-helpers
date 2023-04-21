#!/usr/bin/env python
import re
from re import match

import click


RGX = '(?P<level>#{2,}) (?P<title>.*) <a id="(?P<id>[^"]+)"></a>'


@click.command()
@click.option('-i', '--indent-size', type=int, default=4, help="Indent size (spaces)")
@click.argument('file')
def main(indent_size, file):
    with open(file, 'r') as f:
        for line in f.readlines():
            line = line.rstrip('\n')
            m = match(RGX, line)
            if not m:
                continue
            level, title, id = len(m['level']), m['title'], m['id']
            indent = ' ' * (indent_size * (level - 2))
            title = re.sub(r'\[([^]]+)](?:\([^)]+\))?', r'\1', title)
            print(f'{indent}- [{title}](#{id})')


if __name__ == '__main__':
    main()
