from __future__ import print_function

try:
    raw_input
except NameError:
    raw_input = input

import argparse
import pip
from pkg_resources import working_set, get_distribution


def autoremove(name, yes=False):
    dist = get_distribution(name)
    graph = get_graph()
    dead = find_all_dead(graph, set([dist]))
    print("Uninstalling:")
    show_tree(dist, dead)
    if yes or confirm("Proceed (y/N)?"):
        for d in dead:
            remove_dist(d)


def show_tree(dist, dead, indent=0):
    prefix = ' ' * indent * 4
    print(prefix, end=' ')
    show_dist(dist)
    for req in requires(dist):
        if req in dead:
            show_tree(req, dead, indent + 1)


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
    pip.main(['uninstall', '-y', dist.project_name])
    # Avoid duplicate output caused by pip.logger.consumers being configured
    # over and over again
    pip.logger.consumers = []


def get_graph():
    g = {dist: set() for dist in working_set}
    for dist in working_set:
        for req in requires(dist):
            g[req].add(dist)
    return g


def requires(dist):
    return map(get_distribution, dist.requires())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name')
    parser.add_argument('-y', '--yes', action='store_true')
    args = parser.parse_args()
    autoremove(args.name, args.yes)

if __name__ == '__main__':
    main()
