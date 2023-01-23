#!/usr/bin/env python

from re import match

import click


RGX = '(?P<level>#{2,}) (?P<title>.*) <a id="(?P<id>[^"]+)"></a>'


@click.command()
@click.argument('file')
def main(file):
    with open(file, 'r') as f:
        for line in f.readlines():
            line = line.rstrip('\n')
            m = match(RGX, line)
            if not m:
                continue
            level, title, id = len(m['level']), m['title'], m['id']
            indent = '  ' * (level - 2)
            print(f'{indent}- [{title}](#{id})')


if __name__ == '__main__':
    main()
