from __future__ import print_function

import optparse
import os
import pip
import platform

from pkg_resources import working_set, get_distribution


__version__ = '0.9.1'

try:
    raw_input
except NameError:
    raw_input = input


try:
    dict.iteritems
except AttributeError:

    def iteritems(d):
        return iter(d.items())
else:

    def iteritems(d):
        return d.iteritems()


WHITELIST = ['pip', 'setuptools']

def get_package_manager():
    managers = {
        'rpm'  : ['/etc/redhat-release'],
        'dpkg' : ['/etc/lsb-release', '/etc/debian_version']
    }

    if platform.system() == 'Linux':
        for pkg, files in iteritems(managers):
            for identy in files:
                if os.path.isfile(identy):
                    return pkg


def get_package(dist):
    try:
        manager = get_package_manager()
        egg = os.path.join(dist.location, (dist.egg_name() + '.egg-info'))

        if manager == 'rpm':
            import rpm

            ts = rpm.TransactionSet()
            return ",".join([n['name'] for n in ts.dbMatch('basenames', egg)])

        if manager == 'dpkg':
            # TODO: Add dpkg support
            pass

    except ImportError:
        pass

def autoremove(names, yes=False):
    dead = list_dead(names)
    if dead and (yes or raw_input("Uninstall (y/N)?") == 'y'):
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
    show_dist(dist, get_package(dist))
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


def show_dist(dist, pkg=None):
    if pkg:
        print('*> %s %s (%s) (Package: %s)' % (dist.project_name,
            dist.version, dist.location, pkg))
    else:
        print('%s %s (%s)' % (dist.project_name, dist.version, dist.location))


def remove_dist(dist):
    if not get_package(dist):
        pip.main(['uninstall', '-y', dist.project_name])
        # Avoid duplicate output caused by pip.logger.consumers being configured
        # over and over again
        pip.logger.consumers = []
    else:
        print("Skiped %s, module installed from package" % dist.project_name)


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
