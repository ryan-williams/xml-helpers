#!/usr/bin/env python
import html
from sys import stdin

import click


@click.command()
@click.argument('strs', nargs=-1)
def main(strs):
    if not strs:
        strs = ( line.rstrip('\n') for line in stdin.readlines() )
    for s in strs:
        print(html.unescape(s))


if __name__ == '__main__':
    main()
