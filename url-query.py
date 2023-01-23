#!/usr/bin/env python
import json
from sys import stdin
from urllib.parse import urlparse, parse_qs

import click


@click.command()
@click.option('-p', '--param')
@click.argument('strs', nargs=-1)
def main(param, strs):
    if not strs:
        strs = ( line.rstrip('\n') for line in stdin.readlines() )
    for s in strs:
        query = parse_qs(urlparse(s).query)
        if param:
            vs = query[param]
            if len(vs) > 1:
                raise RuntimeError(f'Got {len(vs)} "{param}" params: {vs}')
            if not vs:
                print()
                continue
            [v] = vs
            print(v)
        else:
            print(json.dumps(query))


if __name__ == '__main__':
    main()
