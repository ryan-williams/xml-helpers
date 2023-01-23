#!/usr/bin/env python
import re
import sys
from os.path import splitext
from tempfile import TemporaryDirectory
from typing import Union, Optional
from urllib.parse import parse_qs, urlparse

import click
import lxml.html
from lxml.html import tostring


def stderr(msg=''):
    sys.stderr.write(msg)
    sys.stderr.write('\n')


def camel_case(s):
    def upper_first(pc):
        return pc[0].upper() + pc[1:]
    return ''.join([
        upper_first(pc) if idx else pc
        for idx, pc in enumerate(re.split('[-_:]', s))
    ])


DEFAULT_ATTR_MAP = {
    'xlink:href': 'href',
    'preserveaspectratio': 'preserveAspectRatio',
    'viewbox': 'viewBox',
}
DEFAULT_TAG_MAP = {
    'clippath': 'clipPath',
}


def rewrite_attributes(
        tree,
        attr_map: Optional[Union[bool, dict]] = None,
        tag_map: Optional[Union[bool, dict]] = None,
        unwrap_google_redirects=True,
):
    attr_map = attr_map or DEFAULT_ATTR_MAP
    tag_map = tag_map or DEFAULT_TAG_MAP

    for node in tree.iter():
        if tag_map is not False and node.tag in tag_map:
            node.tag = tag_map[node.tag]

        if attr_map is not False:
            attrib = node.attrib
            for k, v in attrib.items():
                k2 = attr_map.get(k, camel_case(k))
                if k != k2:
                    stderr(f'Node {node}: rewriting {k} to {k2}')
                    del attrib[k]
                    attrib[k2] = v

        if unwrap_google_redirects:
            attrib = node.attrib
            href = attrib.get('href')
            if not href:
                continue
            p = urlparse(href)
            if f'{p.netloc}{p.path}' != 'www.google.com/url':
                continue
            query = parse_qs(p.query)
            [new_href] = query['q']
            attrib['href'] = new_href

    return tree


@click.command()
@click.option('-G', '--no-google-redirect-rewrites', is_flag=True)
@click.option('-P', '--no-pretty-print', is_flag=True)
@click.argument('svg_path', required=True)
@click.argument('out_path', required=False)
def main(no_google_redirect_rewrites, no_pretty_print, svg_path, out_path):
    pretty_print = not no_pretty_print
    name, ext = splitext(svg_path)
    if not out_path:
        out_path = f'{name}.out{ext}'

    html = lxml.html.parse(svg_path)
    svg = list(html.getroot().iter('svg'))[0]
    rewrite_attributes(svg, unwrap_google_redirects=not no_google_redirect_rewrites)
    s = tostring(svg, method='xml', pretty_print=True).decode()
    if out_path == '-':
        sys.stdout.write(s)
    else:
        with open(out_path, 'w') as f:
            f.write(out_path)
    #     with TemporaryDirectory() as tmpdir:
    #         tmp_path = f'{tmpdir}/out{ext}'
    #         html.write(tmp_path, pretty_print=pretty_print)
    #         with open(tmp_path, 'r') as f:
    #             sys.stdout.write(f.read())
    # else:
    #     html.write(out_path, pretty_print=pretty_print)


if __name__ == '__main__':
    main()
