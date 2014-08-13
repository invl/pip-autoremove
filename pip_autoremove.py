import os
import argparse

from pkg_resources import working_set, get_distribution


def autoremove(name, yes=False):
    dead = find_all_dead(get_distribution(name))
    print("Uninstalling:")
    map(show_dist, dead)
    if yes or confirm("Proceed (y/N)?"):
        map(remove_dist, dead)


def find_all_dead(start):
    g = get_graph()
    dead = set([start])
    while True:
        new = set(find_dead(g, dead))
        if not new:
            break
        dead |= new
    return dead


def find_dead(graph, dead):
    for node, succ in graph.items():
        if node not in dead:
            # We only care about leaves killed by us
            if succ and not (succ - dead):
                yield node


def confirm(prompt):
    return raw_input(prompt) == 'y'


def show_dist(dist):
    print('%s %s (%s)' % (dist.project_name, dist.version, dist.location))


def remove_dist(dist):
    os.system('pip uninstall -y %s' % dist.project_name)


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
