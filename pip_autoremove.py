from __future__ import print_function

import optparse
import subprocess

from pkg_resources import working_set, get_distribution


__version__ = '0.9.1'

try:
    raw_input
except NameError:
    raw_input = input


WHITELIST = ['pip', 'setuptools']


def autoremove(names, yes=False):
    dead = list_dead(names)
    if dead and (yes or confirm("Uninstall (y/N)?")):
        for d in dead:
            remove_dist(d)


def list_dead(names):
    start = set(map(get_distribution, names))
    graph = get_graph()
    dead = exclude_whitelist(find_all_dead(graph, start))
    for d in start:
        show_tree(d, dead)
    return dead


def exclude_whitelist(dists):
    return set(dist for dist in dists if dist.project_name not in WHITELIST)


def show_tree(dist, dead, indent=0, visited=None):
    if visited is None:
        visited = set()
    if dist in visited:
        return
    visited.add(dist)
    print(' ' * 4 * indent, end='')
    show_dist(dist)
    for req in requires(dist):
        if req in dead:
            show_tree(req, dead, indent + 1, visited)


def find_all_dead(graph, start):
    return fixed_point(lambda d: find_dead(graph, d), start)


def find_dead(graph, dead):

    def is_killed_by_us(node):
        succ = graph[node]
        return succ and not (succ - dead)

    return dead | set(filter(is_killed_by_us, graph))


def fixed_point(f, x):
    while True:
        y = f(x)
        if y == x:
            return x
        x = y


def confirm(prompt):
    return raw_input(prompt) == 'y'


def show_dist(dist):
    print('%s %s (%s)' % (dist.project_name, dist.version, dist.location))


def remove_dist(dist):
    subprocess.check_call(["pip", "uninstall", "-y", dist.project_name])


def get_graph():
    g = dict((dist, set()) for dist in working_set)
    for dist in working_set:
        for req in requires(dist):
            g[req].add(dist)
    return g


def requires(dist):
    return map(get_distribution, dist.requires())


def main(argv=None):
    parser = create_parser()
    (opts, args) = parser.parse_args(argv)
    if opts.leaves:
        list_leaves()
    elif opts.list:
        list_dead(args)
    else:
        autoremove(args, yes=opts.yes)


def get_leaves(graph):

    def is_leaf(node):
        return not graph[node]

    return filter(is_leaf, graph)


def list_leaves():
    graph = get_graph()
    for node in get_leaves(graph):
        show_dist(node)


def create_parser():
    parser = optparse.OptionParser(
        usage='usage: %prog [OPTION]... [NAME]...',
        version='%prog ' + __version__,
    )
    parser.add_option(
        '-l', '--list', action='store_true', default=False,
        help="list unused dependencies, but don't uninstall them.")
    parser.add_option(
        '-L', '--leaves', action='store_true', default=False,
        help="list leaves (packages which are not used by any others).")
    parser.add_option(
        '-y', '--yes', action='store_true', default=False,
        help="don't ask for confirmation of uninstall deletions.")
    return parser


if __name__ == '__main__':
    main()
